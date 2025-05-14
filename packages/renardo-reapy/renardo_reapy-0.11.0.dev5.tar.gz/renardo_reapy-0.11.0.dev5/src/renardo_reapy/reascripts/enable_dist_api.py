"""
Enable ```reapy`` distant API.

Running this ReaScript from inside REAPER allows to import ``reapy``
from outside. It creates a persistent Web Interface inside REAPER and
adds the ReaScript ``renardo_reapy.reascripts.activate_reapy_server`` to the
Actions list. Importing ``reapy`` from outside REAPER will trigger
the latter **via** the Web Interface.
"""

if __name__ == "__main__":
    import renardo_reapy.runtime as runtime
    runtime.config.enable_dist_api()
