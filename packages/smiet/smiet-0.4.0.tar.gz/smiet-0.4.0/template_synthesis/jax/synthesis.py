from __future__ import annotations

import logging
import os
from functools import partial
from typing_extensions import Self, Tuple

import h5py
import jax
import jax.numpy as jnp
from interpax import interp1d

from .io import BaseShower, SlicedShower
from .utilities import jax_utils, units
from .utilities.atmosphere import Atmosphere
from .utilities.coordinate_transformations import spherical_to_cartesian
from .utilities.geometry import angle_between


def amplitude_function(
    params: jax.typing.ArrayLike,
    frequencies: jax.typing.ArrayLike,
    d_noise: float = 0.0,
) -> jax.Array:
    """
    Calculate the amplitude frequency spectrum corresponding to the parameters `params`.

    Parameters
    ----------
    params : jax.typing.ArrayLike
        The spectral parameters. If it is a multidimensional array, the first dimension must contain the parameters.
    frequencies : jax.typing.ArrayLike
        The values of the frequencies to evaluate - remove central frequency beforehand!
    d_noise : float, default=0.0
        The noise floor level

    Returns
    -------
    The evaluated amplitude frequency spectrum with shape VIEW x FREQ x SLICES
    """
    if len(params.shape) == 1:
        params = params.reshape((params.shape[0], 1))
    return (
        params[0, :, None, :]
        * jnp.exp(
            params[1, :, None, :] * frequencies[None, :, None]
            + params[2, :, None, :] * frequencies[None, :, None] ** 2
        )
        + d_noise
    )


class TemplateSynthesis(metaclass=jax_utils.ModelMeta):
    """Class to manage the template synthesis."""

    def __init__(self: Self, atm_model: int = 17, freq_ar: list = None) -> None:
        self.logger = logging.getLogger(
            "template_synthesis.jax.synthesis.TemplateSynthesis"
        )
        self.atm = Atmosphere(atm_model, observation_level=0.0)

        # spectral parameters
        self.has_spectral_coefficients = None
        self.geo = None
        self.ce = None
        self.ce_lin = None
        self.viewing_angles = None

        # frequency properties
        self.frequency_range = None
        self.frequencies = None
        self.freq_range_mask = None
        self.truncated_frequencies = None

        # antenna properties
        self.ant_names = None
        self.ant_time_axes = None
        self.ant_positions = None

        # slice properties
        self.template_information = None
        self.grammages = None
        self.nr_slices = None

        # read spectral parameters from file
        if freq_ar is not None:
            spectral_filename = f'spectral_parameters_{int(freq_ar[0])}_{int(freq_ar[1])}_{int(freq_ar[2])}.hdf5'
            self.read_spectral_file(spectral_filename)

    def read_spectral_file(
        self: Self,
        filename: str
    ) -> None:
        """
        Read spectral parameters from a file with `filename` in the spectral_parameters/ directory.

        Parameters
        ----------
        filename : str
           The name of the spectral parameters file
        """
        path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spectral_parameters', filename)

        if not os.path.exists(path_to_file):
            raise FileNotFoundError(
                f"Filename {filename} does not exist in the spectral_parameters/ directory."
                "Did you provide the correct frequency range?"
            )

        # read spectral parmaeters from hdf5 file
        with h5py.File(path_to_file) as spectral_file:
            self.frequency_range = tuple(
                spectral_file['/Metadata/Frequency_MHz'][:] * units.MHz
            )
            self.viewing_angles = jnp.array(
                spectral_file["/Metadata/ViewingAngles"][:]
            )

            self.geo = jnp.array(
                spectral_file["SpectralFitParams/GEO"][:]
            )
            self.ce = jnp.array(
                spectral_file["SpectralFitParams/CE"][:]
            )
            self.ce_lin = jnp.array(
                spectral_file["SpectralFitParams/CE_LIN"][:]
            )

            self.has_spectral_coefficients = True

        self.logger.debug(f"Loaded in the spectral coefficients from {filename}")

    def make_template(self: Self, origin: SlicedShower, ce_linear: bool = True) -> None:
        """
        Process a ``SlicedShower`` into a template.

        Parameters
        ----------
        origin : template_synthesis.jax.io.sliced_shower.SlicedShower
            The origin shower
        ce_linear : bool, default=True
            Whether to use linear variant of the CE component correction
        """
        if not self.has_spectral_coefficients:
            raise RuntimeError(
                "Please make sure the spectral coefficients are loaded before making a template"
            )

        # initialise all antenna parameters
        self._initialise_antennas(origin)

        self.logger.info(f"Using CE_LIN for synthesis: {ce_linear}")

        # initialise parameters
        self.freq_range_mask = jnp.logical_and(
            self.frequency_range[0] <= self.frequencies,
            self.frequencies <= self.frequency_range[1],
        )
        self.truncated_frequencies = (
            self.frequencies[self.freq_range_mask] - self.frequency_range[2]
        )

        # gather shower parameters to compute the relevant shower properties
        self.grammages = origin.grammages
        self.nr_slices = origin.nr_slices

        # computing shower properties (distance, correction factors, normalisation factors)
        ant_distances_origin, correction_factors_origin, norm_factors_origin = (
            self._compute_shower_properties(
                origin,
                ce_linear,
            )
        )

        # set inverse of normalisation factor to zero where particles are too small so as to not process those slices
        norm_factors_origin_inv = jnp.where(
            norm_factors_origin == 0, 0.0, 1.0 / norm_factors_origin
        )

        # get traces from the origin shower
        # {GEO, CE} x ANT x SAMPLES x SLICES
        geo_origin, ce_origin = origin.get_traces(return_start_time=False)
        origin_traces = jnp.array([geo_origin, ce_origin])
        # filter out traces outside the grammage limit

        # RFFT traces to frequency domain, half of traces (+1) due to taking only the real part of FT
        # {GEO, CE} x ANT x FREQ x SLICES
        origin_traces_fft = jnp.fft.rfft(origin_traces, norm="ortho", axis=2)
        origin_traces_fft *= (
            ant_distances_origin[None, :, None, :]
            * norm_factors_origin_inv[:, None, None, :]
        )

        # amplitude and phase arrays
        # {GEO, CE} x ANTENNAS x FREQUENCIES x SLICES
        self.amplitudes = jnp.abs(origin_traces_fft) * correction_factors_origin
        self.phases = jnp.angle(origin_traces_fft)

        # store the shower properties in template_information
        self.template_information = {
            "zenith": origin.zenith,
            "azimuth": origin.azimuth,
            "xmax": origin.xmax,
            "nmax": origin.nmax,
            "geomagnetic_angle": origin.geomagnetic_angle,
        }

    @partial(jax.jit, static_argnames=["ce_linear"])
    def map_template(
        self: Self, target: BaseShower, ce_linear: bool = False
    ) -> jax.Array:
        """
        Map the template to a target profile, represented in a target BaseShower.

        Calculates the trace for every antenna present in the template.

        Parameters
        ----------
        target : BaseShower
            The target BaseShower object, containing the longitudinal profile,
            zenith, azimuth, geomagnetic angle, xmax and nmax

        Returns
        -------
        total_synth : jax.Array
            The synthesised geomagnetic & charge-excess trace for all antennas.
            Shape is {GEO, CE} x ANT x SAMPLES
        """
        # some assertions
        # TODO: figure out how to apply JIT with this

        # # # 1st assert to ensure that the slice width are the same
        # assert (
        #     target.slice_grammage == jnp.diff(self.grammages)[0]
        # ), f"slice width must be the same between origin : {jnp.diff(self.grammages)} and target : {target.slicing_grammage} shower."

        # # second assertion: to ensure that the number of slices between
        # # target and origin are the same
        # assert (
        #     target.nr_slices == self.nr_slices
        # ), f"Number of slices between target {target.nr_slices} and origin {self.nr_slices} must be equal!"

        # computing shower properties (distance, correction factors, normalisation factors)
        ant_distances_target, correction_factors_target, norm_factors_target = (
            self._compute_shower_properties(
                target,
                ce_linear,
            )
        )

        # same shape as amplitudes, {GEO, CE} x ANT x FREQ x SLICES
        target_amplitudes = (
            self.amplitudes
            * norm_factors_target[:, None, None, :]
            / ant_distances_target[None, :, None, :]
        )

        # take into account corresction factors
        target_amplitudes /= jnp.where(
            correction_factors_target == 0, 1.0, correction_factors_target
        )

        synthesised_traces = jnp.fft.irfft(
            target_amplitudes * jnp.exp(1j * self.phases),
            norm="ortho",
            axis=2,  # inverse FFT on frequency axis
        )  # shape same as sliced traces, {GEO, CE} x ANT x SAMPLES x SLICES

        # total synthesised trace is the sum over all slices
        total_synth = jnp.sum(
            synthesised_traces,
            axis=-1,
        )
        return total_synth

    def _calculate_distance_viewing_angles(
        self: Self,
        zenith: float,
        azimuth: float,
    ) -> tuple[jax.Array, jax.Array]:
        """
        Calculate the viewing angles of the saved antenna's with respect to the slice, as well as their distance to this slice.

        Parameters
        ----------
        zenith : float
            the zenith angle in deg
        azimuth : float
            the azumithal angle in deg.

        Return
        ------
        vangles, distances : jax.Array
            tuple of viewing angles (units in Cherenkov angle) and distances (units of m)
            for all antennas
        """
        # geometric distance from each slice, shape of ANT x SLICES x 3
        dis_from_slices = jnp.expand_dims(
            self.atm.get_geometric_distance_grammage(self.grammages, zenith / units.rad)
            * units.m,
            axis=(0, 2),
        )

        # shower axis as a unit vector, also with shape of ANT x SLICES x 3
        unit_shower_axis = jnp.expand_dims(
            spherical_to_cartesian(zenith / units.rad, azimuth / units.rad), axis=(0, 1)
        )

        # slices as vectors, shape with ANT x SLICES x 3
        slice_vectors = unit_shower_axis * dis_from_slices

        # shape of ANT x SLICES x 3, need to expand antenna positions since
        # only defined as ANT x 3
        slice_to_ant_vectors = self.ant_positions[:, None, :] - slice_vectors

        # viewing angles and distances returns ANTs x SLICES
        vangles = (
            angle_between(slice_to_ant_vectors, -1 * slice_vectors)
            / self.atm.get_cherenkov_angle(self.grammages, zenith / units.rad)[None, :]
            * units.rad
        )
        distances = jnp.linalg.norm(slice_to_ant_vectors, axis=-1)

        return vangles, distances

    def _get_spectra(
        self: Self, xmax: float, freq: jax.typing.ArrayLike
    ) -> tuple[jax.Array, jax.Array, jax.Array]:
        r"""
        Retrieve the amplitude spectra at the specified frequencies, for a given :math:`\Delta X_{max}`.

        Parameters
        ----------
        xmax : float
            The maximum of the atmospheric depth in g/cm^2
        freq : jax.typing.ArrayLike
            The list of frequencies at which to evaluate the spectra

        Returns
        -------
        spectrum_geo : jax.typing.ArrayLike
            The evaluated geomagnetic amplitude frequency spectrum, shaped as (# viewing angles, # freq).
        spectrum_ce : jax.typing.ArrayLike
            The charge-excess spectrum
        spectrum_ce_lin : jax.typing.ArrayLike
            The charge-excess spectrum, but evaluated without the quadratic (`c`) component.
        """
        # expand dimensions for grammage to VIEW x FREQ x SLICES
        gram = jnp.expand_dims(self.grammages, axis=(0, 1))
        # NB: flip in the spectral parameters is necessary since
        # jnp.polyval evaluates from from the HIGHEST power,
        # whereas np.polynomial.polynomial.polyval evaluates from
        # the LOWEST power.
        # since the amplitude function follows the structure from the
        # numpy code, we need another flip after evaluating the polynomial
        spectral_params_geo = jnp.flip(
            jnp.polyval(jnp.flip(self.geo.T)[..., None], gram - xmax), axis=(0, 1)
        )  # 3 x viewing angles x SLICES
        spectral_params_ce = jnp.flip(
            jnp.polyval(jnp.flip(self.ce.T)[..., None], gram - xmax), axis=(0, 1)
        )  # 3 x viewing angles x SLICES
        spectral_params_ce_lin = jnp.flip(
            jnp.polyval(jnp.flip(self.ce_lin.T)[..., None], gram - xmax), axis=(0, 1)
        )  # 3 x viewing angles x SLICES

        return (
            amplitude_function(spectral_params_geo, freq / units.MHz),
            amplitude_function(spectral_params_ce, freq / units.MHz),
            amplitude_function(spectral_params_ce_lin, freq / units.MHz),
        )

    def _initialise_antennas(self: Self, shower: SlicedShower) -> None:
        """
        Initialise the parameters for the antenna.

        This is just a convenience function to make the make_template function look better.

        Parameters
        ----------
        shower : template_synthesis.jax.io.sliced_shower.SlicedShower
            The sliced shower object conatining antennas information
        """
        self.ant_names = list(shower.ant_names)

        # convert position to NRR CS, with shape ANT x 3
        # self.ant_positions = jnp.array(list(shower.ant_dict.values()))[:, [1, 0, 2]]
        self.ant_positions = jnp.array(list(shower._ant_positions_ground))[:, [1, 0, 2]]
        self.ant_positions = self.ant_positions.at[:, 0].set(
            self.ant_positions[:, 0] * -1
        )

        # Calculate frequencies from shower
        dt_res = shower.get_coreas_settings()["time_resolution"]
        self.frequencies = jnp.fft.rfftfreq(shower.trace_length, d=dt_res)

        # get time axes, with shape ANT x SAMPLES
        _, _, shower_start_times = shower.get_traces(return_start_time=True)
        self.ant_time_axes = (
            shower_start_times[..., None]
            + dt_res * jnp.arange(shower.trace_length)[None, :]
        )

    @partial(jax.jit, static_argnames=["ce_linear"])
    def _compute_shower_properties(
        self: Self,
        shower: BaseShower,
        ce_linear: bool = True,
    ) -> Tuple[jax.Array, jax.Array, jax.Array]:
        """
        Compute properties of the shower for all grammages.

        In particular, get the correction factors within the frequency range of interest
        and calculate the distance & viewing angle for all slices and antennas

        Convenience function since the same things are being called for the target
        and origin shower.

        Parameters
        ----------
        shower : BaseShower
            container for air shower containing
            (zenith, azimuth, geomagnetic angle, xmax, nmax, nparts_per_slice)
        ce_linear : bool, default=True
            flag to use the linearised charge-excess emission or not

        Returns
        -------
        ant_distances : jax.Array
            distance from slice to each antenna in m
            Shaped as ANT x SLICES
        correction_factors : jax.Array
            correction factors for the coefficients.
            Shaped as {GEO, CE} x ANT x FREQ x NSLICES
        norm_factors : jax.Array
            the normalisation factors applied to the template amplitude
            Shaped as {GEO x CE} x NSLICES
        """
        # frequencies corresponding to the frequency range of interest
        frequencies = self.frequencies[self.freq_range_mask] - self.frequency_range[2]

        # viewing angle and distance in shape of ANT x SLICES
        ant_v_angles, ant_distances = self._calculate_distance_viewing_angles(
            shower.zenith, shower.azimuth
        )
        self.logger.debug("Computed distance & viewing angles")

        # amplitude spectrum computed at each viewing angle & frequency
        # in shape ANGLES x FREQ x SLICES
        geo, ce, ce_lin = self._get_spectra(shower.xmax, frequencies)
        ce = ce_lin if ce_linear else ce
        self.logger.debug("Computed amplitude spectrum")

        # calculate the correction factors
        # shape is {GEO x CE} x ANTS x FREQ x SLICES
        correction_factors = jnp.zeros(
            (2, len(self.ant_names), len(self.frequencies), self.nr_slices)
        )

        for icomp, comp in enumerate([geo, ce]):
            # 1. take log for more accurate interpolation (after taking abs to avoid -log values)
            # 2. expand dimension on second to last axis for antenna information to make
            #    shape of VIEW x FREQ x ANTS x SLICES
            # 3. repeat all elements in the antenna axis to make it compatible with interp1d
            corr_fact = jnp.expand_dims(
                jnp.log(jnp.where(jnp.abs(comp[:-2]) <= 1e-20, 1.0, jnp.abs(1.0 / comp[:-2]))),  # Temporary fix bad viewing angles in large freq range
                axis=2,
            )
            corr_fact = jnp.repeat(
                corr_fact,
                repeats=len(self.ant_names),
                total_repeat_length=len(self.ant_names),
                axis=2,
            )

            # 1. expand viewing angle dimension to match the shape of correction factor
            # 2. take exponential to evaluate the log from the correction factor
            correction_factors = correction_factors.at[
                icomp, :, self.freq_range_mask, :
            ].set(
                jnp.exp(
                    interp1d(
                        xq=jnp.expand_dims(ant_v_angles, axis=(0, 1)),
                        x=self.viewing_angles[:-2],
                        f=corr_fact,
                        method="cubic2",
                        extrap=jnp.array([corr_fact[0, ...], corr_fact[-1, ...]]),
                    )
                )
            )

        self.logger.debug("Computed correction factors")

        # normalisation factors
        # first entry for normlisation of geomagnetic emission using geomagnetic angle / density
        # second entry same for C-E emission, which is just sin(cherenkov angle)
        # also expand dimensions of nparts per slice to get shape of {GEO,CE} x SLICES
        norm_factors = jnp.array(
            [
                jnp.sin(shower.geomagnetic_angle)
                / self.atm.get_density(self.grammages, shower.zenith / units.rad),
                jnp.sin(
                    self.atm.get_cherenkov_angle(
                        self.grammages, shower.zenith / units.rad
                    )
                    * units.rad
                ),
            ]
        ) * jnp.expand_dims(shower.nparts_per_slice, axis=0)
        # remove slices with few particles
        norm_factors = jnp.where(
            shower.nparts_per_slice < 0.001 * shower.nmax, 0, norm_factors
        )

        self.logger.debug("Computed normalisation factors")

        return (
            ant_distances,
            correction_factors,
            norm_factors,
        )

    def save_template(
        self: Self,
        template_file: str = "default_template.h5",
        save_dir: str = os.path.join(os.path.dirname(__file__), "..", "templates"),
    ) -> None:
        """
        Save the internal state of the synthesis class to disk.

        Parameters
        ----------
        template_file : str, default='default_template.h5'
            the file to save the template into
        save_dir : str, default='template_synthesis/templates'
            the directory to save the template into
        """
        with h5py.File(os.path.join(save_dir, template_file), "w") as f:
            prop_grp = f.create_group("shower")
            prop_grp.create_dataset("zenith", data=self.template_information["zenith"])
            prop_grp.create_dataset(
                "azimuth", data=self.template_information["azimuth"]
            )
            prop_grp.create_dataset(
                "geomagnetic_angle", data=self.template_information["geomagnetic_angle"]
            )
            prop_grp.create_dataset("xmax", data=self.template_information["xmax"])
            prop_grp.create_dataset("nmax", data=self.template_information["nmax"])

            ant_grp = f.create_group("antennas")
            ant_grp.create_dataset("ant_names", data=self.ant_names)
            ant_grp.create_dataset("ant_positions", data=self.ant_positions)
            ant_grp.create_dataset("ant_time_axes", data=self.ant_time_axes)

            freq_grp = f.create_group("frequencies")
            freq_grp.create_dataset("frequency_range", data=self.frequency_range)
            freq_grp.create_dataset("frequencies", data=self.frequencies)
            freq_grp.create_dataset("frequency_mask", data=self.freq_range_mask)
            freq_grp.create_dataset("trunc_frequency", data=self.truncated_frequencies)

            spect_grp = f.create_group("spect_params")
            spect_grp.create_dataset("geo", data=self.geo)
            spect_grp.create_dataset("ce", data=self.ce)
            spect_grp.create_dataset("ce_lin", data=self.ce_lin)
            spect_grp.create_dataset("viewing_angles", data=self.viewing_angles)

            slice_grp = f.create_group("atm_slice")
            slice_grp.create_dataset("grammages", data=self.grammages)
            slice_grp.create_dataset("nr_slices", data=self.nr_slices)

            templ_grp = f.create_group("template")
            templ_grp.create_dataset("amplitudes", data=self.amplitudes)
            templ_grp.create_dataset("phases", data=self.phases)

    def load_template(
        self: Self,
        template_file: str = "default_template.h5",
        save_dir: str = os.path.join(os.path.dirname(__file__), "..", "templates"),
    ) -> None:
        """
        Load the template from a saved state, as done by save_template().

        Parameters
        ----------
        template_file : str, default='default_template.h5'
            the file to save the template into
        save_dir : str, default='template_synthesis/templates'
            the directory to save the template into
        """
        file_path = os.path.join(save_dir, template_file)
        # verify that the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Template file {file_path} does not exist.")

        with h5py.File(file_path, "r") as f:
            self.ant_names = f["antennas/ant_names"][()]
            self.ant_positions = f["antennas/ant_positions"][()]
            self.ant_time_axes = f["antennas/ant_time_axes"][()]

            self.frequency_range = f["frequencies/frequency_range"][()]
            self.frequencies = f["frequencies/frequencies"][()]
            self.freq_range_mask = f["frequencies/frequency_mask"][()]
            self.truncated_frequencies = f["frequencies/trunc_frequency"][()]

            self.geo = f["spect_params/geo"][()]
            self.ce = f["spect_params/ce"][()]
            self.ce_lin = f["spect_params/ce_lin"][()]
            self.viewing_angles = f["spect_params/viewing_angles"][()]

            self.grammages = f["atm_slice/grammages"][()]
            self.nr_slices = f["atm_slice/nr_slices"][()]

            self.amplitudes = f["template/amplitudes"][()]
            self.phases = f["template/phases"][()]

            self.template_information = {
                "zenith": f["shower/zenith"][()],
                "azimuth": f["shower/azimuth"][()],
                "geomagnetic_angle": f["shower/geomagnetic_angle"][()],
                "xmax": f["shower/xmax"][()],
                "nmax": f["shower/nmax"][()],
            }

    def get_time_axis(self: Self) -> jax.Array:
        """
        Get the time axis for all antennas.

        Returns
        -------
        time_axis : np.ndarray
            The time axis for each antenna, shaped as (# antennas, # time samples)

        """
        # return self.ant_information['time_axis']
        return self.ant_time_axes

    def get_ant_names(self: Self) -> list[str]:
        """
        Get the names of all internal antennas.

        Returns
        -------
        ant_names : list of str

        """
        # return self.ant_information['name']
        return self.ant_names
