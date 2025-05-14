import logging
from typing_extensions import Self, Tuple, Union

import h5py
import jax
import jax.numpy as jnp
from scipy.constants import c as c_vacuum

from ..utilities import units
from ..utilities.atmosphere import Atmosphere
from ..utilities.coordinate_transformations import (
    cstrafo,
    e_to_geo_ce,
)
from .base_shower import BaseShower

logger = logging.getLogger("template_synthesis.jax.io")


def filter_trace(
    trace: jax.typing.ArrayLike,
    trace_sampling: float,
    f_min: float,
    f_max: float,
    sample_axis: int = 0,
) -> jax.Array:
    """
    Filter the trace within the frequency domain of interest.

    Parameter:
    ----------
    trace : jax.typing.ArrayLike
        The trace to filter. Shape is SAMPLES x ...
    trace_sampling : float
        The sampling rate of the traces
    f_min : float
        The minimum frequency in which to filter, in MHz
    f_max : float
        The maximum frequency in which to filter, in MHz
    sample_axis : int, default=0
        The axis in which the filtering takes place. Default is 0, i.e. the first axis

    Returns
    -------
    filtered_trace : jax.Array
        The filtered trace within the requested frequency domain
    """
    # Assuming `trace_sampling` has the correct internal unit, freq is already in the internal unit system
    freq = jnp.fft.rfftfreq(trace.shape[sample_axis], d=trace_sampling)
    freq_range = jnp.logical_and(freq > f_min, freq < f_max)

    # Find the median maximum sample number of the traces
    max_indces = jnp.median(jnp.argmax(trace, axis=sample_axis))
    to_roll = jnp.int32(trace.shape[sample_axis] / 2 - max_indces)

    # Roll all traces such that max is in the middle
    roll_pulse = jnp.roll(trace, to_roll, axis=sample_axis)

    # FFT, filter, IFFT
    spectrum = jnp.fft.rfft(roll_pulse, axis=sample_axis)
    spectrum = jnp.apply_along_axis(
        lambda ax: ax * jnp.int32(freq_range), sample_axis, spectrum
    )
    filtered = jnp.fft.irfft(spectrum, axis=sample_axis)

    return jnp.roll(filtered, -to_roll, axis=sample_axis)


class SlicedShower(BaseShower):
    """
    Class to read in showers from each slice from CoREAS simulations, inherited from BaseShower.

    Parameters
    ----------
    file_path : str
        The filepath to the simulation to read.
    slicing_grammage : int, default=5
        The width between atmospheric slices in g/cm^2
    atm_model : int, default=17
        The atmospheric model used. Default is 17, which is the
        US standard atmosphere. See utilities/atmosphere/atm_models.py
        for all possible atmospheric models.
    slice_trace : Union[int, None], default = None
        The index to slice the trace. Used to reduce the number of samples
        by removing `slice_trace` numbers of samples.
        Default is None, which uses the full time trace
    slice_ant : Union[int, None], default = None
        The index to slice the antennas. Used to reduce the number of antennas
        by removing `slice_ant` numbers for antennas between distance from the core.
        This is done to have coveraage for all distances from the core.
        Default is None, which uses all antennas in the dataset.
    """

    def __init__(
        self: Self,
        file_path: str,
        slicing_grammage: int = 5,
        atm_model: int = 17,
        slice_trace: Union[int, None] = None,
        slice_ant: Union[int, None] = None,
    ) -> None:

        super().__init__()

        self.logger = logging.getLogger("template_synthesis.jax.io.SlicedShower")

        self.__slice_gram = slicing_grammage  # g/cm2, TODO: change how to read this since its fixed from filepath
        self.__file = file_path  # input file path

        self._trace_length = None

        self.ant_names = None
        self.ant_dict = {}

        self._ant_positions_ground = None
        self._trace_slices = None
        self._GH_parameters = None

        self.__parse_hdf5(atm_model, slice_trace, slice_ant)

        # define transformation container here
        self.transformer = cstrafo(
            self.zenith / units.rad,
            self.azimuth / units.rad,
            magnetic_field_vector=self._magnetic_field,
        )

    def __parse_hdf5(
        self: Self,
        atm_model: int = 17,
        slice_trace: Union[int, None] = None,
        slice_ant: Union[int, None] = None,
    ) -> None:
        file = h5py.File(self.__file)

        # antenna properties
        self.ant_names = list(
            sorted(set([key.split("x")[0] for key in file["CoREAS"]["observers"].keys()]))
        )

        # antenna positions at the ground
        self._ant_positions_ground = jnp.array(
            [
                file["CoREAS"]["observers"][f"{ant_name}x{self.__slice_gram}"].attrs[
                    "position"
                ]
                * units.cm
                for ant_name in self.ant_names
            ]
        )  # antennas x 3

        self._magnetic_field = jnp.array(
            [
                0,
                file["inputs"].attrs["MAGNET"][0],
                -1 * file["inputs"].attrs["MAGNET"][1],
            ]
        )  # magnetic field value
        self._simulation_core = (
            jnp.array(
                [
                    -1 * file["CoREAS"].attrs["CoreCoordinateWest"],
                    file["CoREAS"].attrs["CoreCoordinateNorth"],
                    file["CoREAS"].attrs["CoreCoordinateVertical"],
                ]
            )
            * units.cm
        )
        dis_to_core = jnp.sqrt(
            jnp.sum(
                jnp.abs(self.core[:2] - self._ant_positions_ground[:, :2])
                ** 2,
                axis=-1
            )
        )

        # order antennas based on distance from the shower core
        self.ant_names = [self.ant_names[int(iant)] for iant in jnp.argsort(dis_to_core)]
        self._ant_positions_ground = self._ant_positions_ground[jnp.argsort(dis_to_core), :]
        self.dis_to_core = dis_to_core[jnp.argsort(dis_to_core)]

        # TODO: remove this when the fourier interpolation is implemented, then we would not need it
        if slice_ant is not None:

            # generate indices so that we sample each 9th of the footprint so that we cover the full
            # footprint
            nant_slice = len(self.ant_names) // 8
            indices = jnp.concatenate([jnp.arange(i, len(self.ant_names), nant_slice) for i in range(nant_slice)], dtype=int)


            self.dis_to_core = self.dis_to_core[indices][:slice_ant]
            self.ant_names = [self.ant_names[idx] for idx in indices][:slice_ant]
            self._ant_positions_ground = self._ant_positions_ground[indices, :][:slice_ant, :]

        # radio emission properties
        self.geometry = self.get_geometry(file)  # zenith & azimuth

        # longitudinal profile
        long_profile = file["atmosphere"]["NumberOfParticles"][:]

        grammages = long_profile[:, 0]
        nparts_per_slice = jnp.sum(long_profile[:, 2:4], axis=1)

        self.atm = Atmosphere(model=atm_model, observation_level=self.core[2] / units.m)

        # filter out grammages that will reach beyond earth
        grammage_lim_mask = grammages <= self.atm.get_xmax_from_distance(
            0.0,
            self.zenith / units.rad,
        )

        self.grammages = grammages[grammage_lim_mask]
        self.nparts_per_slice = nparts_per_slice[grammage_lim_mask]

        # Below not needed, but kept incase its required again
        # in order: [N, X0, Xmax, p0, p1, p2] (p0,p1,p2 are the polynomail coefficients in denominator for lambda)
        self._GH_parameters = jnp.array(
            file["atmosphere"].attrs["Gaisser-Hillas-Fit"]
        )  # GH parameters from fit

        self.trace_slices = jnp.array(
            [
                [
                    file["CoREAS"]["observers"][f"{ant_name}x{int(gram):d}"][:]
                    for ant_name in self.ant_names
                ]
                for gram in self.grammages
            ]
        )  # slices x antennas x samples x 4

        # map it to the correct shape of 
        # 4 x ANT x SAMPLES x SLICE as according to numpy version
        self.trace_slices = jnp.moveaxis(self.trace_slices, (0,1,2,3), (3,1,2,0))

        # TODO: again remove in the future when we apply the response model
        if slice_trace is not None:
            self.trace_slices = self.trace_slices[..., :slice_trace, :]
        self._trace_length = self.trace_slices.shape[2]
        self._dt = self.get_coreas_settings()["time_resolution"]

        file.close()

    @property
    def trace_length(self: Self) -> int:
        """Length of the trace."""
        return self._trace_length

    @property
    def name(self: Self) -> str:
        return self.__file.split("/")[-1].split(".")[0]

    @staticmethod
    def get_geometry(file: h5py.File) -> Tuple[float, float]:
        """Retrieve the geometry (zenith, angle) in degrees."""
        zenith = file["inputs"].attrs["THETAP"][0] * units.deg
        azimuth = (
            file["inputs"].attrs["PHIP"][0] * units.deg - 90 * units.deg
        )  # transform to radiotools coord
        return zenith, azimuth

    def filter_trace(
        self: Self, trace: jax.typing.ArrayLike, f_min: float, f_max: float,
    ) -> jax.Array:
        """
        Filter the trace until we get traces that match the frequency interval.

        This implementation only works consistently with a 1-D array, but a TODO would be 
        to allow this to work with multidimensional arrays.

        Parameters
        ----------
        trace : jax.typing.ArrayLike
            The unfiltered electric field trace.
            NOTE: TRACE MUST BE IN FIRST AXIS!
        f_min : float
            The minimum frequency in which we want to filter the trace
        f_max : float
            The maximum frequency in which we want to filter the trace

        Returns
        -------
        filtered_trace : jax.Array
            The trace that is filtered between the frequency range [f_min, f_max]
        """
        trace_axis = 0  # based on self.get_trace()
        if trace.shape[trace_axis] != self._trace_length:
            logger.warning(
                "Trace shape does not match recorded trace length along the last axis"
            )
            logger.info("Attempting to find the trace axis...")
            for shape_i in range(len(trace.shape)):
                if trace.shape[shape_i] == self._trace_length:
                    logger.info(f"Found axis {shape_i} which matches trace length!")
                    trace_axis = shape_i
                    break
        return filter_trace(
            trace,
            self._dt,
            f_min,
            f_max,
            sample_axis=trace_axis,
        )

    def get_traces(
        self: Self, return_start_time: bool = False
    ) -> Union[Tuple[jax.Array, jax.Array, jax.Array], Tuple[jax.Array, jax.Array]]:
        """
        Get all traces for all antennas.

        Parameters
        ----------
        return_start_time : bool, default=False
            If True, an array containing the time of the first sample
            of all slices is returned

        Returns
        -------
        trace_geo : jax.Array
            The geomagnetic trace in shapes ANT x SAMPLES x SLICES
        trace_ce : jax.Array
            The charge-excess trace in shapes ANT x SAMPLES x SLICES
        trace_start_time : jax.Array (returned only if return_start_times is True)
            The time of the first sample of the trace of size N_SLICES x ANT
        """
        # antenna in the shower plane, in shape of ANT x POS
        # transpose since last axis must be position axis
        antenna_vvB = self.transformer.transform_to_vxB_vxvxB(
            jnp.array(
                [
                    -self._ant_positions_ground[:, 1] - self.core[0],
                    self._ant_positions_ground[:, 0] - self.core[1],
                    self._ant_positions_ground[:, 2] - self.core[2],
                ]
            ).T,
        )

        # Save trace start time for all antennas
        # we assume ultra-relativisitic for all signals s.t. signals arrive from all slices
        # at the same time
        # -> just take mean of each trace slice
        trace_start_times = jnp.mean(self.trace_slices[0, :, 0, :], axis=-1) * units.s
        # Convert CGS to internal units
        # and re-define them in NRR coordinates
        # shape must be such that position is in last axis
        # shape returned as SLICES x SAMPLES x ANT x POS
        trace_slice_ground = (
            jnp.array(
                [
                    -self.trace_slices[2, ...],
                    self.trace_slices[1, ...],
                    self.trace_slices[3, ...],
                ]
            )
            * c_vacuum
            * 1e2
            * units.microvolt
            / units.m
        ).T

        # transform from ground -> shower plane
        # shape as SLICES x SAMPLES x ANT x POS
        trace_slice_vvB = self.transformer.transform_to_vxB_vxvxB(trace_slice_ground)

        # unit of pos does not matter, this is divided away
        # make the dimension of antenna positions same as the trace for multiplication
        # shape returned as SLICES x SAMPLES x ANT for geo and ce
        trace_geo, trace_ce = e_to_geo_ce(
            trace_slice_vvB,
            antenna_vvB[None, None, :, 0],
            antenna_vvB[None, None, :, 1],
        )

        # finally transpose to get the right shape
        # of ANT x SAMPLES x SLICES
        trace_geo, trace_ce = trace_geo.T, trace_ce.T

        # we want to return it as shape ANT x SAMPLES x SLICES
        if return_start_time:
            return trace_geo, trace_ce, trace_start_times

        return trace_geo, trace_ce

    def get_coreas_settings(self: Self) -> dict:
        """Get specific configurations from the CoREAS simulation that is useful for the synthesis.

        Returns
        -------
        coreas_settings : dict
            A dictionary containing important information about the configuration of the CoREAS simulation
        """
        file = h5py.File(self.__file)

        time_resolution = float(file["CoREAS"].attrs["TimeResolution"]) * units.s

        return {"time_resolution": time_resolution}
