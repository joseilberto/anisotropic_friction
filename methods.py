def init_wrapper(*args):
    def outer_wrapper(function):
        def inner_wrapper():
            for idx, arg in enumerate(args):
                if idx == 0:
                    args_parse = arg()
                else:
                    arg()
            return function(args_parse)
        return inner_wrapper
    return outer_wrapper
