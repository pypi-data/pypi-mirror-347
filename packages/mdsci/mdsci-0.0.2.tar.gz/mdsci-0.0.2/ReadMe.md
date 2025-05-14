# MdSci: Extended Markdown format for scientific writing

MdSci, or Markdown Scientific, is an extended Markdown syntax primarily designed for scientific writing.

- [Features](#features)
- [Installation Guide](#installation-guide)
- [Developer Guide](#developer-guide)
- [License](#license)

## Features

MdSci is build on the top of the document converting tool [Pandoc](https://pandoc.org/), so all Markdown syntax supported by Pandoc can also be used in MdSci.

Apart from that, MdSci mainly include a style of new syntax starting with double-semicolons, like `;;foo{arg, key1=value1}`. See the documentation for more details.


## Installation Guide

Install the mdsci package on your Python.

```
pip install -U mdsci
```

You can easily call `mdsci` from the command line:

```
mdsci input.md
```

Note that the above command will automatically copy the CSS file from the package into the current folder. In this example, it will be named as `input-mdsci.css`.


## Developer Guide

A script file `make.py` is provided for easier development. Remember to check the followings before using the script:

* Build: Edit the `version` (e.g., `1.0.0rc1`) in `pyproject.toml`.
* Upload: Prepare a `.pypirc` file with `__token__` as username and API token as password.

To build, update and test the developing version:
```
# In the venv environment
python make.py --build
python make.py --update  # Choose local wheel
mdsci test.md
```

Then we can use `--testpypi` or `--pypi` command to upload. Check `--help` of `make.py` for more details.

## License

[MIT](./LICENSE)
