import contextlib
import functools
import importlib

import renardo_reapy
import renardo_reapy.config
from renardo_reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning
from .network import machines
# if not renardo_reapy.is_inside_reaper():
#     try:
#         from .network import Client, WebInterface
#         _WEB_INTERFACE = WebInterface(renardo_reapy.config.WEB_INTERFACE_PORT)
#         _CLIENT = Client(_WEB_INTERFACE.get_reapy_server_port())
#     except DisabledDistAPIError:
#         import warnings
#         warnings.warn(DisabledDistAPIWarning())
#         _CLIENT = None


def dist_api_is_enabled():
    """Return whether reapy can reach REAPER from the outside."""
    return machines.get_selected_client() is not None


class inside_reaper(contextlib.ContextDecorator):

    """
    Context manager for efficient calls from outside REAPER.

    It can also be used as a function decorator.

    Examples
    --------
    Instead of running:

    >>> project = renardo_reapy.Project()
    >>> l = [project.bpm for i in range(1000)

    which takes around 30 seconds, run:

    >>> project = renardo_reapy.Project()
    >>> with renardo_reapy.inside_reaper():
    ...     l = [project.bpm for i in range(1000)
    ...

    which takes 0.1 seconds!

    Example usage as decorator:

    >>> @renardo_reapy.inside_reaper()
    ... def add_n_tracks(n):
    ...     for x in range(n):
    ...         renardo_reapy.Project().add_track()

    """

    def __call__(self, func, encoded_func=None):
        if renardo_reapy.is_inside_reaper():
            return func
        if isinstance(func, property):
            return DistProperty.from_property(func)
        # Check if the decorated function is from renardo_reapy
        module_name = func.__module__
        if module_name == 'reapy' or module_name.startswith('renardo_reapy.'):
            @functools.wraps(func)
            def wrap(*args, **kwargs):
                f = func if encoded_func is None else encoded_func
                client = machines.get_selected_client()
                return client.request(f, {"args": args, "kwargs": kwargs})
            return wrap
        # Otherwise, use the context manager
        return super().__call__(func)

    def __enter__(self):
        if not renardo_reapy.is_inside_reaper():
            machines.get_selected_client().request("HOLD")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not renardo_reapy.is_inside_reaper():
            machines.get_selected_client().request("RELEASE")
        return False


class DistProperty(property):

    _inside_reaper = inside_reaper()

    @classmethod
    def from_property(cls, p):
        return cls().getter(p.fget).setter(p.fset).deleter(p.fdel)

    @staticmethod
    def _encode(f, method_name):
        return {
            "__callable__": True,
            "module_name": f.__module__,
            "name": "{}.f{}".format(f.__qualname__, method_name)
        }

    def getter(self, fget):
        if fget is not None:
            fget = self._inside_reaper(fget, self._encode(fget, "get"))
        return super().getter(fget)

    def setter(self, fset):
        if fset is not None:
            fset = self._inside_reaper(fset, self._encode(fset, "set"))
        return super().setter(fset)

    def deleter(self, fdel):
        if fdel is not None:
            fdel = self._inside_reaper(fdel, self._encode(fdel, "del"))
        return super().deleter(fdel)
