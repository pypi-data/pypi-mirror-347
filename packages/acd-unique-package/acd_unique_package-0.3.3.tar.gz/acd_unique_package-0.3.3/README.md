[![PyPI version](https://badge.fury.io/py/acd_unique_package.svg)](https://badge.fury.io/py/acd_unique_package)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/acd_unique_package)
![Linux](https://img.shields.io/badge/os-Linux-blue.svg)
![macOS Intel](https://img.shields.io/badge/os-macOS_Intel-lightgrey.svg)
![macOS ARM](https://img.shields.io/badge/os-macOS_ARM-lightgrey.svg)

# Python Packaging Example


### If you like the repo, it would be awesome if you could add a star to it! It really helps out the visibility.

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Development/Contributing](#developmentcontributing)
* [License](#license)

## Package Description

Prints my name, and it my first package!

## Usage

from a script:

```python
from acd_unique_package import Acd

Acd().print_name()
```

From the command line:

```bash
acd_unique_package
```

## Installation

Install python and pip if you have not already.

Then run:

```bash
pip3 install pip --upgrade
pip3 install wheel
```

For production:

```bash
pip3 install acd_unique_package
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/aykcandem/acd_unique_package.git
cd acd_unique_package
pip3 install -e .[dev]
```

To test the development package: [Testing](#testing)


## Development/Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Test it
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin my-new-feature`
7. Ensure github actions are passing tests
8. Email me at test@gmail.com if it's been a while and I haven't seen it

## License

BSD License (see license file)