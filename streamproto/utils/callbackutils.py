def callbacks(fn_list: list):
    def f():
        for fn in fn_list:
            fn()
    return f
