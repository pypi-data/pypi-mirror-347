# Contributing to `renardo_reapy`

First, thanks for being interested in contributing to `renardo_reapy`!

There are several ways you can contribute to the project:
1. [Reporting bugs](#reporting-bugs)
2. [Requesting features](#requesting-features)
3. [Improving documentation](#improving-documentation)
4. [Adding features](#adding-features)

## Providing feedback

### Reporting bugs

Some features of `renardo_reapy` may have been too quickly tested and have bugs. Don't hesitate to report them by creating an issue.

### Requesting features

The API doesn't cover the whole ReaScript API yet. If some features are critical to you, please open an issue. It will help prioritize future work.

## Extending the source code

Direct contributions to the code are warmly welcomed. You can contribute by hitting the **Fork** button in the top right corner of the project page.

### Improving documentation

Documentation aims to follow the [numpy docs convention](https://docs.scipy.org/doc/numpy/docs/howto_document.html#numpydoc-docstring-guide). Yet the docstrings are far from correct for now, so feel free to improve them.

### Adding features

There are two ways of adding features:

1. wrapping ReaScript API (*i.e.* pick a ReaScript API function and include it in `renardo_reapy`),
2. extending the API beyond ReaScript (*i.e.* building new features that you find the ReaScript API misses).

In both cases, the code should:
- follow PEP style conventions as much as possible. You can check your code is PEP-compliant with the Python package [pycodestyle](https://pypi.org/project/pycodestyle/).
- follow the change log convention [here](https://keepachangelog.com/en/1.0.0/). Basically, all changes to the API (addition, removal, or bug fixes) must be reported in the `Unreleased` section of [CHANGELOG.md](CHANGELOG.md) under the corresponding subsections (`Added`, `Removed`, `Fixed`, etc.).

#### A note about type hints (`.pyi` files)

We try to make the use of type checkers (such as [mypy](http://mypy-lang.org/)) compatible with reapy. Each reapy module `module.py` thus has a corresponding `module.pyi` file that contains type hints.

However, support for type hinting is not our top priority. Thus, if you don't master type hinting, but still want to contribute, feel free to only change the `.py` files. We will take care of making the corresponding `.pyi` changes afterwards.
