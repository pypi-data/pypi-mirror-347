import os
import numpy as np

import radiotools.helper as hp
from radiotools.atmosphere.models import Atmosphere

from template_synthesis.utilities import units
from template_synthesis.corsika.generate_file_contents import generate_list_file, generate_reas_file, generate_inp_file, \
    generate_list_file_cherenkov, CORSIKA_PARTICLE_CODES


# Functions to generate all files for a single simulation

def generate_simulation(sim_nr, sim_primary, sim_cores,
                        sim_zenith=None, sim_azimuth=None, sim_energy=None,
                        slice_gram=5.0 * units.g / units.cm2,
                        magnetic_field='lofar',
                        thinning=1e-6, atmosphere=17,
                        core=None, radii=None,
                        cherenkov=False):
    """
    Prepare the contents for the INP, LIST and REAS files for a sliced MPI simulation,
    with a star shape pattern for the antenna layout.

    One can choose to project the antennas along the shower axis or along the viewing angle by
    setting the `cherenkov` option. If this is set to True, the `radii` parameter will be interpreted
    as a list of viewing angles expressed as multiples of the slice Cherenkov angle. Otherwise,
    the `radii` parameter should be the list of radii to use in the star shape
    (use this option to generate origin showers).

    The magnetic field vector can be taken from the `radiotools.helper` module, by passing a string
    as the `magnetic_field` parameter. This variable is passed on to the
    `radiotools.helper.get_magnetic_field_vector` function. But to be consistent with the
    CORSIKA definition where the magnetic field has no East-West component, the vector x-component
    is set to zero. This ensures the simulated antennas are indeed on the (vx)vxB axis.

    As of November 2024, only proton, helium, carbon, silicon and iron primaries are supported
    (this is limited by the CORSIKA particle codes defined in the `generate_file_contents.py` file).

    Parameters
    ----------
    sim_nr : int
        The number of the simulation.
    sim_primary : {'proton', 'helium', 'carbon', 'silicon', 'iron'}
        The primary particle to inject
    sim_cores : int
        The number of cores the simulation will be run on
    sim_zenith : float, optional
        The zenith angle. If not provided, the angle will be drawn from `sample_zenith_angle`.
    sim_azimuth : float, optional
        The azimuth angle. If not provided, the angle will be drawn from `sample_azimuth_angle`.
    sim_energy : float, optional
        The energy of the simulation. If not provided, the energy will be drawn from `sample_primary_energy`.
    core : list of float, default=[0, 0, 0] * units.m
        The core to use in the simulation
    slice_gram : float, default=5.0 * units.g / units.cm2
        The thickness of the atmospheric slices
    radii : list of float, default=None
        The radii of the starshape, passed to `template_synthesis.corsika.generate_list_file`
    cherenkov : bool, default=False
        If True, interpret `radii` as multiples of slice Cherenkov radius, and calculate antenna radii per slice
    magnetic_field : np.ndarray or str, default='lofar'
        If a string, the name of the site from which to take the magnetic field vector (using radiotools.helper).
        Otherwise, this is interpreted as the magnetic field vector (in internal units).
    thinning : float, default=1e-7
        The thinning level to use
    atmosphere : int, default=17
        The CORSIKA atmosphere identifier
    """
    assert sim_primary in CORSIKA_PARTICLE_CODES, f'Primary {sim_primary} not supported!'

    if core is None:
        core = np.array([0., 0., 0.]) * units.m

    sim_zenith = sample_zenith_angle()[0] if sim_zenith is None else sim_zenith
    sim_azimuth = sample_azimuth_angle()[0] if sim_azimuth is None else sim_azimuth
    sim_primary_energy = sample_primary_energy()[0] if sim_energy is None else sim_energy

    atm = Atmosphere(atmosphere, curved=False)
    grammage_ground = atm.get_distance_xmax(sim_zenith / units.rad, 0.0,
                                            observation_level=core[2] / units.m)
    slice_gram /= (units.g / units.cm2)
    grammage_slices = np.arange(0.0, (grammage_ground // slice_gram + 1) * slice_gram + 1, slice_gram)
    grammage_slices *= (units.g / units.cm2)

    if type(magnetic_field) is str:
        magnetic_field_vector = hp.get_magnetic_field_vector(magnetic_field) * np.array([0, 1, 1]) * units.gauss
    else:
        magnetic_field_vector = np.asarray(magnetic_field)

    inp_file = generate_inp_file(
        sim_nr,
        sim_zenith, sim_azimuth,
        sim_primary_energy,
        obs_lev=core[2],
        primary=sim_primary,
        n_cores=sim_cores,
        thin=thinning,
        atm=atmosphere,
        magnet=magnetic_field_vector,
        slicing=slice_gram * (units.g / units.cm2)  # make sure it is passed in internal units!
    )
    if cherenkov:
        list_file = generate_list_file_cherenkov(
            sim_zenith, sim_azimuth, grammage_slices,
            atm, radii,
            magnet_vector=magnetic_field_vector, core=core,
            number_of_arms=1,
        )
    else:
        list_file = generate_list_file(
            sim_zenith, sim_azimuth, grammage_slices,
            magnet_vector=magnetic_field_vector,
            core=core,
            radii=radii,
            number_of_arms=1,
        )
    reas_file = generate_reas_file(
        sim_nr, core=core
    )

    return inp_file, list_file, reas_file


def write_simulation_to_file(inp_file, list_file, reas_file, sim_directory='./'):
    """
    Write the contents of the INP, LIST and REAS files for an MPI simulation to a directory.
    The function will fail if the directory already exists.

    Parameters
    ----------
    inp_file : list
        The contents of the INP file
    list_file : list
        The contents of the LIST file
    reas_file : list
        The contents of the REAS file
    sim_directory : str, default='./'
        The path to the directory where the simulation directory will be made, in which all files are written
    """
    sim_nr = int(inp_file[0].split(' ')[-1][:-1])

    sim_directory = os.path.join(sim_directory, f'SIM{sim_nr:06d}')

    if os.path.exists(sim_directory):
        raise FileExistsError('Directory for simulation already exists! Aborting...')
    else:
        os.mkdir(sim_directory)

    with open(f'{sim_directory}/SIM{sim_nr:06d}.inp', 'w+') as file:
        file.writelines(inp_file)

    with open(f'{sim_directory}/SIM{sim_nr:06d}.list', 'w+') as file:
        file.writelines(list_file)

    with open(f'{sim_directory}/SIM{sim_nr:06d}.reas', 'w+') as file:
        file.writelines(reas_file)


# Function to sample input parameters

def sample_primary_energy(exp_range=(8, 10)):
    r"""
    Sample a single primary energy from log-uniform distribution, between the exponents given
    by `exp_range`. For example, using the default settings, calling this function will generate
    a value between :math:`10^{8}` and :math:`10^{10}` GeV.

    Parameters
    ----------
    exp_range : tuple, default=(8, 10)
        The lower and upper exponent of the energy range in GeV to sample from

    Returns
    -------
    primary_energy : float
        Primary energy (in internal units)
    """
    primary_energy_exp = np.random.uniform(*exp_range, size=1)  # random exponent in GeV

    return 10 ** primary_energy_exp * units.GeV


def sample_zenith_angle(range=(0, 90), size=1, uniformity='sin2'):
    r"""
    Sample the zenith angle from some distribution normalised with the solid angle.
    The names of the distributions refer to the variable in which they are uniform.

    Parameters
    ----------
    range : tuple, default=(0, 90)
        The lower and upper zenith angle in degrees (endpoints exclude
    size : int, default=1
        The number of angles to samples
    uniformity : {'sin2', 'sin', 'cos'}
        The distribution to use to sample the zenith angle

    Returns
    -------
    zenith_angle : float
        Sampled zenith angle (in internal units)

    Notes
    -----
    The names of the distributions refer to the variable in which they are uniform,
    in the sense that if you sampled using 'sin2' (the default), the zenith angle
    distribution will look uniform if binned in :math:`sin^2(\theta)`.
    """
    rng = np.random.default_rng()

    possible_theta = np.arange(*range, 0.001)[1:-2]  # exclude 0 and 90 degrees to avoid problems with sin and division
    possible_theta *= units.deg

    if uniformity == 'sin':
        # Probability distribution = sin(theta), normalised
        my_p = np.cos(possible_theta)
        my_p /= np.sum(my_p)
    elif uniformity == 'sin2':
        my_p = np.sin(2 * possible_theta)
        my_p /= np.sum(my_p)
    elif uniformity == 'cos-1':
        # return np.arccos(1 - rng.random(size=size))
        my_p = np.sin(possible_theta)
        my_p /= np.sum(my_p)

    return rng.choice(possible_theta, p=my_p, size=size) * units.deg


def sample_azimuth_angle(range=(0, 360), size=1):
    """
    Sample the azimuth angle within the given range, from a uniform distribution.

    Parameters
    ----------
    range : tuple, default=(0, 360)
        The lower and upper azimuth angle in degrees
    size : int, default=1
        The number of angles to samples

    Returns
    -------
    azimuth_angle : float
        Sampled azimuth angle (in internal units)
    """
    rng = np.random.default_rng()

    return rng.uniform(*range, size=size) * units.deg
