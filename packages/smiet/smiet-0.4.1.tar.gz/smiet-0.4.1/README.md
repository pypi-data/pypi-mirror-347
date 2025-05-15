# Welcome to the SMIET software!

The **SMIET** (**S**ynthesis **M**odelling **I**n-air **E**mission using **T**emplates) - pronounced "s-meet" - implements the template synthesis algorithm.
This framework is used to synthesise the radio emission from cosmic ray air showers using semi-analytical relations extracted from a set of Monte-Carlo showers.
It is described in more detail in [this publication](url).

This repository implements the operations necessary to perform the synthesis. 
We have two versions, one in plain Numpy and another one wrapped in JAX with higher performance. 
The latter is mostly meant to be used in the context of Information Field Theory.

## Citing

If you use this software in a publication, please cite this [Zenodo entry](https://doi.org/10.5281/zenodo.15194465).
### References

- Proof of concept publication in [Astroparticle physics](https://doi.org/10.1016/j.astropartphys.2023.102923)
- Proceedings of [ARENA22](https://pos.sissa.it/424/052/)
- Proceedings of [ICRC23](https://pos.sissa.it/444/216/)

## Documentation

The online documentation can be found [here](https://web.iap.kit.edu/huege/smiet/).

### Installation
The package is written in Python, so in order to use it it is recommended to have virtual environment with the necessary packages.
These are specified in the `pyproject.toml` file, such that the package can be installed using pip as

```bash
pip install .
```

To install the JAX version, you can use the optional `jax` keyword,

```bash
pip install .[jax]
```

There is also the optional `tests` keyword, which will install `matplotlib`.

### Dependencies

The lowest Python version with which we tested the package is Python 3.8. It might also work with Python 3.7, there are no big show stoppers in terms of packages.

These are the packages on which the Numpy version relies:

- `radiotools`
- `Numpy`
- `Scipy`
- `h5py`
- `typing-extensions`

For the JAX version, the following packages will also be installed:

- `jax`
- `jaxlib`

### Usage

After installing the library, you can start by running the scripts in the [demo]() folder to get acquainted with the template synthesis syntax.
You can also refer to the [documentation](https://homepage.iihe.ac.be/~mitjadesmet/).

## Support and development

In case of issues, please open an issue in this repository.
You are also welcome to open merge requests in order to introduce changes.
Any contributions are greatly appreciated!

For other inquiries, please contact <mitja.desmet@vub.be> or <keito.watanabe@kit.edu>.

### Roadmap

Currently the code contains all the classes necessary to load in sliced shower simulations and perform the template synthesis operations.
These include normalisation of the amplitude spectra with respect to the geometry, as well as the arrival time shifts applied to the phase spectra.
The next steps are now to:

1. Add rigorous unit tests
2. Improve the way in which showers and template information is stored
3. Add extensive documentation
4. Achieve parity between the Numpy and JAX versions

## Authors and acknowledgment

We appreciate all who have contributed to the project.

- Mitja Desmet, for the development of the template synthesis algorithm and the Numpy implementation
- Keito Watanabe, for implementing the JAX version
- Ruben Bekaert, for suggesting changes to the Numpy interface

## License

This repository is licensed under the GPLv3.