import logging
from typing_extensions import Self

import jax
import jax.numpy as jnp

from ..utilities import units
from ..utilities.coordinate_transformations import spherical_to_cartesian
from ..utilities.geometry import angle_between
from ..utilities.jax_utils import ModelMeta

logger = logging.getLogger("template_synthesis.jax.io")


class BaseShower(metaclass=ModelMeta):
    """
    Base class to contain the shower parameters.

    The Shower class is used to hold the geometric information for a shower, like the zenith/azimuth,
    as well as the longitudinal profile. It can be used to specify the target parameters for a shower
    in template synthesis.
    """

    __parameter_names = ("xmax", "nmax", "zenith", "azimuth", "magnetic_field")

    def __init__(self: Self) -> None:
        self.logger = logging.getLogger("template_synthesis.jax.io.Shower")

        # shower parameters
        self._xmax = None
        self._nmax = None
        self._grammages = None
        self._nparts_per_slice = None
        self._nr_slices = None
        self.__slice_gram = 5

        # observational parameters
        self._geometry = None  # (zenith, angle)
        self._magnetic_field = None
        self._simulation_core = jnp.array([0, 0, 0])  # Currently fixed

    @property
    def xmax(self: Self) -> float:
        """The $X_{max}$ of the shower, from fitting a GH to the longitudinal profile."""
        if self._xmax is not None:
            return self._xmax
        elif self._GH_parameters is not None:
            return self._GH_parameters[2]
        else:
            self.logger.error("The Gaisser-Hillas parameters have not been set")

    @property
    def nmax(self: Self) -> float:
        """The $N_{max}$ of the shower, from fitting a GH to the longitudinal profile."""
        if self._nmax is not None:
            return self._nmax
        elif self._GH_parameters is not None:
            return self._GH_parameters[0]
        else:
            self.logger.error("The Gaisser-Hillas parameters have not been set")

    @xmax.setter
    def xmax(self: Self, xmax: float) -> None:
        self._xmax = xmax

    @nmax.setter
    def nmax(self: Self, nmax: float) -> None:
        self._nmax = nmax

    @property
    def grammages(self: Self) -> jax.Array:
        """Array of atmospheric slices in g/cm^2."""
        if self._grammages is not None:
            return self._grammages
        else:
            self.logger.error("The grammage has not been set")

    @property
    def slice_grammage(self: Self) -> float:
        """The spacing between each grammage in g/cm^2."""
        if self._grammages is not None:
            return self._grammages[1] - self._grammages[0]
        else:
            self.logger.error(
                "Longitudinal profile has not been set yet, cannot calculate slicing thickness"
            )

    @property
    def nparts_per_slice(self: Self) -> float:
        """The number of particles in each slice."""
        if self._nparts_per_slice is not None:
            # ensure that the length of grammages and _nparts_per_slice is the same
            assert len(self._nparts_per_slice) == len(
                self._grammages
            ), "Length not same as grammages!"
            return self._nparts_per_slice
        else:
            self.logger.error("Set the longitudinal parameters first.")

    @property
    def nr_slices(self: Self) -> int:
        """The number of slices in the array."""
        if self._nparts_per_slice is not None or self.grammages is not None:
            # ensure that the length of grammages and _nparts_per_slice is the same
            assert len(self._nparts_per_slice) == len(
                self._grammages
            ), "Length not same as grammages!"
            return len(self._nparts_per_slice)
        else:
            self.logger.error("Set the longitudinal parameters first.")

    @grammages.setter
    def grammages(self: Self, grammages: jax.typing.ArrayLike) -> None:
        self._grammages = grammages

    @nparts_per_slice.setter
    def nparts_per_slice(self: Self, nparts_per_slice: jax.typing.ArrayLike) -> None:
        self._nparts_per_slice = nparts_per_slice

    @property
    def geometry(self: Self) -> jax.Array:
        """Store the zenith and azimuth. These must be provided in the internal units system."""
        if self._geometry is not None:
            return self._geometry
        else:
            self.logger.error("Geometry has not been set")

    @property
    def zenith(self: Self) -> float:
        """The zenith angle in degrees."""
        if self._geometry is not None:
            return self._geometry[0]
        else:
            self.logger.error("Geometry has not been set")

    @property
    def azimuth(self: Self) -> float:
        """The azimuthal angle in degrees."""
        if self._geometry is not None:
            return self._geometry[1]
        else:
            self.logger.error("Geometry has not been set")

    @geometry.setter
    def geometry(self: Self, geo: jax.typing.ArrayLike) -> None:
        assert (
            len(geo) == 2
        ), "Please provide zenith and azimuth components in internal units"

        self._geometry = jnp.array(geo)

    @property
    def core(self: Self) -> jax.Array:
        """The core (x, y, z in NRR CS) where the EAS hit in the simulation."""
        if self._simulation_core is not None:
            return self._simulation_core
        else:
            self.logger.error("The simulation core is not known")

    @property
    def magnet(self: Self) -> float:
        """Magnetic field vector in the NRR coordinate system."""
        if self._magnetic_field is not None:
            return self._magnetic_field
        else:
            self.logger.error("The magnetic field vector has not been set")

    @magnet.setter
    def magnet(self: Self, magnet_field_vec: jax.typing.ArrayLike) -> None:
        assert (
            len(magnet_field_vec) == 3
        ), "B-field vector must contain three components"

        self._magnetic_field = magnet_field_vec

    @property
    def geomagnetic_angle(self: Self) -> float:
        """The angle between the magnetic field vector and the shower axis."""
        shower_axis = spherical_to_cartesian(*self.geometry / units.rad)

        return angle_between(self.magnet * -1, shower_axis)

    def set_parameters(
        self: Self, grammages: jax.typing.ArrayLike, params: dict
    ) -> None:
        """
        Set the parameters of the shower model from a dictionary of parameters.

        Parameter:
        ----------
        grammages : jax.typing.ArrayLike
            an array of atmospheric depth in g/cm^2
        params : dict
            a dictionary containing values of all parameters.
            this includes:
            - Xmax in g/cm^2 (key: "xmax")
            - Nmax (key: "nmax")
            - zenith angle in degrees (key : "zenith")
            - azimuthal angle in degrees (key : "azimuth")
            - magnetic field vector in jax.typing.ArrayLike (key : "magnetic_field")

            The function will raise an error if any of these parameters are
            not contained in the dictionary with the specific key.
        """
        # assert list(params.keys()) != list(
        #     self.__parameter_names
        # ), "Parameter names (dict keys) are not assigned correctly."

        self.grammages = grammages

        self._xmax = params["xmax"]
        self._nmax = params["nmax"]
        self._geometry = jnp.array([params["zenith"], params["azimuth"]])
        self._magnetic_field = params["magnetic_field"]
