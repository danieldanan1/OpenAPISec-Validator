menu = None
count = 0


def debug(func):
    def inner(*args,**kwargs):
        global count
        count+=1
        if menu.verbose:
            print(count*" " ,f"before: {func.__name__}, args: {args[-1].args}, path: {args[0].path}")
        var = func(*args,**kwargs)
        if menu.verbose:
            print(count*" " ,f"after: {var}-->belong to func name: {func.__name__}")
        count -= 1

        return var
    return inner