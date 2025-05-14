"""
Activate ``renardo_reapy`` server.

Running this ReaScript from inside REAPER sets the ``renardo_reapy`` server
that receives and executes API calls requests from outside. It will
automatically be run when importing ``renardo_reapy`` from outside, if it is
enabled.
"""

import pathlib
import site
import sys

try:
    import renardo_reapy.runtime as runtime
except ImportError:
    reapy_path = pathlib.Path(sys.path[0]).resolve().parent.parent
    sys.path.append(str(reapy_path))
    import renardo_reapy.runtime as runtime

from renardo_reapy.tools.network import Server


def run_main_loop():
    # Get new connections
    SERVER.accept()
    # Process API call requests
    requests = SERVER.get_requests()
    results = SERVER.process_requests(requests)
    SERVER.send_results(results)
    # Run main_loop again
    runtime.defer(run_main_loop)


def get_new_renardo_reapy_server():
    server_port = runtime.config.REAPY_SERVER_PORT
    runtime.set_ext_state("renardo_reapy", "server_port", server_port)
    server = Server(server_port)
    return server


if __name__ == "__main__":
    SERVER = get_new_renardo_reapy_server()
    run_main_loop()
    runtime.at_exit(runtime.delete_ext_state, "renardo_reapy", "server_port")
