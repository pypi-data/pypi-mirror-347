# zzz233

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhusisy%2Fzzz233.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhusisy%2Fzzz233?ref=badge_shield)

**WARNING**: this package is only to demonstrate how to build a minimal python package. Any functions provided in this package could be changed in an incompatible way in the future. DO NOT use it in production.

A minimal python package.

1. download locally
   * clone repository: `git clone git@github.com:husisy/zzz233.git`
   * download zip: `wget xxx`
   * download released package: TODO
2. install
   * install from pypi: `pip install zzz233`
   * install locally: `pip install .`
   * (for developer) install locally: `pip install ".[dev]"`
   * (for documentation developer) install locally: `pip install ".[doc]"`
   * install from github: `pip install git+https://github.com/husisy/zzz233.git`
3. uninstall `pip uninstall zzz233`
4. scrips
   * run in command line: `zzz233`
5. unittest: download locally
   * `pytest`
   * (require developer install locally) coverage `pytest --cov=python/zzz233`
6. documentation
   * build locally: `mkdocs serve`
   * website: `https://husisy.github.io/zzz233/`
7. github action (CI/CD)
   * build documentation, enable github page (select deploy from actions)
   * unittest
8. reading material
   * [github/setuptools_scm](https://github.com/pypa/setuptools_scm) (Source Code Management)
   * [setuptools/pyproject-config](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
   * distribute package to pypi

TODO make a clear table

usage

```Python
# a dummy example
from zzz233 import from_pickle, to_pickle
a = 233
to_pickle(a=a)
assert from_pickle('a')==a
```

TODO

1. [ ] semantic versioning [link](https://semver.org/)

## development

new environment

```bash
micromamba create -n zzz233 python
micromamba activate zzz233

pip install .
# pip install -e ".[dev]"
mkdocs serve
```

publish to pypi

```bash
# cleanup the branch and tag the latest commit with a valid version
# otherwise the build will fail
rm -rf ./dist
pip install build
python -m build

# testpypi
# setup testpypi apikey $HOME/.pypirc (the username is "__token__")
twine upload --repository testpypi dist/*
# --repository-url https://test.pypi.org/legacy/
pip uninstall zzz233
pip install --upgrade -i https://test.pypi.org/simple/ zzz233

# pypi
# --repository-url https://upload.pypi.org/legacy/
```

## Acknowledgements

This project uses the following third-party libraries:

* **h5py**: A Python interface to the HDF5 binary data format. Licensed under the BSD-3-Clause License. [h5py-License](https://github.com/h5py/h5py/blob/master/LICENSE)

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhusisy%2Fzzz233.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhusisy%2Fzzz233?ref=badge_large)
