# renardo_reapy

`renardo_reapy` is a nice pythonic wrapper around the quite unpythonic [ReaScript Python API](https://www.reaper.fm/sdk/reascript/reascripthelp.html#p "ReaScript Python API documentation") for [REAPER](https://www.reaper.fm/ "REAPER").

This is a fork of [python-reapy](https://github.com/RomeoDespres/reapy).

## Contents

1. [Installation](#installation)
2. [Usage](#usage)
    * [ReaScript API](#reascript-api)
    * [`renardo_reapy` API](#reapy-api)
    * [Performance](#performance)
    * [Documentation](#documentation)
3. [Contributing](#contributing)
4. [Author](#author)
5. [License](#license)

## Installation

If you feel you need more explanation than the straightforward instructions below, head to the detailed [installation guide](https://python-renardo_reapy.readthedocs.io/en/latest/install_guide.html).

renardo_renardo_reapy is available via `pip`:

```bash
$ pip install renardo-reapy
```

One additional step is required to let REAPER know renardo_renardo_reapy is available. First, open REAPER. Then in a terminal, run:

```bash
$ python -c "import renardo_reapy.runtime; renardo_reapy.configure_reaper()"
```

Restart REAPER, and you're all set! You can now import `renardo_reapy` from inside or outside REAPER as any standard Python module.

Instead of creating a new ReaScript containing:

```python
from reaper_python import *
RPR_ShowConsoleMsg("Hello world!")
```

you can open your usual Python shell and type:

```python
>>> import renardo_reapy.runtime as runtime
>>> renardo_reapy.print("Hello world!")
```

## Usage

### ReaScript API

All ReaScript API functions are available in `renardo_reapy` in the sub-module `renardo_reapy.reascript_api`. Note that in ReaScript Python API, all function names start with `"RPR_"`. That unnecessary pseudo-namespace has been removed in `renardo_reapy`. Thus, you shall call `renardo_reapy.reascript_api.GetCursorPosition` in order to trigger `reaper_python.RPR_GetCursorPosition`. See example below.

```python
>>> from renardo_reapy import reascript_api as RPR
>>> RPR.GetCursorPosition()
0.0
>>> RPR.SetEditCurPos(1, True, True)
>>> RPR.GetCursorPosition()
1.0
```

Note that if you have the [SWS extension](http://sws-extension.org/) installed, the additional ReaScript functions it provides will be available in `renardo_reapy.reascript_api` and usable inside and outside REAPER as well.

### `renardo_reapy` API

The purpose of `renardo_reapy` is to provide a more pythonic API as a substitute for ReaScript API. Below is the `renardo_reapy` way of executing the example above.

```python
>>> import renardo_reapy.runtime as runtime
>>> project = renardo_reapy.Project() # Current project
>>> project.cursor_position
0.0
>>> project.cursor_position = 1
>>> project.cursor_position
1.0
```
The translation table matches ReaScript functions with their `renardo_reapy` counterparts.

### Performance

When used from inside REAPER, `renardo_reapy` has almost identical performance than native ReaScript API. Yet when it is used from the outside, the performance is quite worse. More precisely, since external API calls are processed in a `defer` loop inside REAPER, there can only be around 30 to 60 of them per second. In a time-critical context, you should make use of the `renardo_reapy.inside_reaper` context manager.

```python
>>> import renardo_reapy.runtime as runtime
>>> project = renardo_reapy.Project() # Current project
>>> # Unefficient (and useless) call
>>> bpms = [project.bpm for _ in range(1000)] # Takes at least 30 seconds...
>>> # Efficient call
>>> with renardo_reapy.inside_reaper():
...     bpms = [project.bpm for _ in range(1000)]
...
>>> # Takes only 0.1 second!

```

A small overhead due to sending function and arguments over the network will still occur each time a `renardo_reapy` function is called from outside REAPER. When running the same function many times in a row (e.g. over a thousand times), using `renardo_reapy.map` may significantly increase performance. See its documentation for more details.

### Documentation

Check the documentation and especially the API guide and Translation Table for more information.

## Contributing

For now, about a half of ReaScript API has a `renardo_reapy` counterpart, the docs are far from great, and many bugs are waiting to be found. Feel free to improve the project by checking the [contribution guide](CONTRIBUTING.md)!

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
