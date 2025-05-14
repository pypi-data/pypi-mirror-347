import sys


def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.

    If ``reapy`` is run from inside a REAPER instance but currently
    controls another REAPER instance on a slave machine (with
    ``runtime.connect``), return False.
    """
    inside = hasattr(sys.modules["__main__"], "obj")
    if not inside:
        return False
    else:
        try:
            return machines.get_selected_machine_host() is None
        except NameError:
            # machines is undefined because we are still in the initial
            # import process.
            return True