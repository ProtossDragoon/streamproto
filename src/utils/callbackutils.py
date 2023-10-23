# Built-In
import functools


def callbacks(fn_list: list):
    def f():
        for fn in fn_list:
            fn()
    return f


def write_json(*args, **kwargs):
    import streamsheet
    @functools.wraps(streamsheet.write_json)
    def f():
        streamsheet.write_json(*args, **kwargs)
    return f
