
This package is developed and maintained by [Poetry](https://python-poetry.org/) with
[Poe the Poet](https://github.com/nat-n/poethepoet).

- [Prerequisite](#prerequisite)
- [Setup](#setup)
  - [Code Quality](#code-quality)
  - [Packaging](#packaging)
- [Usage](#usage)


## Prerequisite
```sh
pip install --upgrade pip
pip install pipx

pipx install poetry
pipx ensurepath
# pipx completions
```

## Setup
### Code Quality
```sh
# set up pre-commit
poetry add pre-commit --dev
poetry run pre-commit install
poetry run pre-commit autoupdate

# set up wily
poetry add wily --dev
poetry run wily setup

poetry run pre-commit run --all-files
```

### Packaging
```sh
# config the package repo
poetry config pypi-token.pypi ${PYPI_TOKEN}
poetry config repositories.pypi "https://dpsauatdk01.intra.hkma.gov.hk:8180/#browse/browse:pypi-hosted"

# build the package
poetry build --output dist
# publish package
poetry publish --repository uat-nexus

PYPI_NAME="default-repo"
poetry config pypi-token.${PYPI_NAME} ${PYPI_TOKEN}
poetry config repositories.${PYPI_NAME} "https://upload.pypi.org/legacy/"
poetry publish --repository ${PYPI_NAME} -vvv
```

## Usage
```sh

```
