import builtins
import functools

import renardo_reapy


@renardo_reapy.inside_reaper()
def map(function, *iterables, constants={}, kwargs_iterable=None):
    """Efficiently map a function to iterables of arguments.

    From outside REAPER, reapy function calls are sent over the
    network for REAPER to execute them. The result in then sent back
    to the reapy client.

    When calling a large number of reapy functions, the network
    overhead can become significant. To solve this problem,
    ``renardo_reapy.map`` sends all arguments at once and retrieves all
    results at once.

    It extends the API of the built-in Python function ``map`` with
    keyword arguments options.

    It stops when the shortest of ``kwargs_iterable`` and all
    iterables in ``iterables`` is exhausted.

    Parameters
    ----------
    function : reapy callable
        Function to map to iterables of arguments.
    iterables : tuple of iterables
        Iterables of arguments that will be iterated in parallel and
        passed to ``function`` as positional arguments.
    constants : dict, optional
        Constant keyword arguments that will be passed  to
        ``function`` at each call.
    kwargs_iterable : iterable of mappings
        Iterable yielding mappings of keyword arguments that will be
        passed to ``function`` alongside the positional arguments in
        ``iterables``.

    Returns
    -------
    list
        The list of results of each calls. Unlike the built-in Python
        function ``map``, it does not return an iterator.

    Examples
    --------
    Below is a simple use case where ``renardo_reapy.map`` reduces run time
    by 95%.

    >>> import time
    >>> import renardo_reapy
    >>>
    >>> project = renardo_reapy.Project()
    >>> take = project.items[0].active_take
    >>> with renardo_reapy.inside_reaper():
    ...     start_time = time.time()
    ...     ppqs = [take.time_to_ppq(time) for time in range(10**5)]
    ...     print(f'Elapsed time without renardo_reapy.map: {time.time() - start_time:.1f} s.')
    ...
    Elapsed time without renardo_reapy.map: 15.0 s.
    >>>
    >>> start_time = time.time()
    >>> ppqs = renardo_reapy.map(take.time_to_ppq, list(range(10**5)))
    >>> print(f'Elapsed time with renardo_reapy.map: {time.time() - start_time:.1f} s.')
    Elapsed time with renardo_reapy.map: 0.7 s.
    """
    if kwargs_iterable is None:
        kwargs_iterable = iter(dict, None)
    partial_function = functools.partial(function, **constants)
    function = lambda *args: partial_function(*args[1:], **args[0])
    return list(builtins.map(function, kwargs_iterable, *iterables))
