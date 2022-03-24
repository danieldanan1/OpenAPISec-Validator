menu = None
count = 0


def debug(func):
    def inner(*args,**kwargs):
        global count
        count+=1
        if menu.verbose:
            print(count*5*" " ,f"before: {func.__name__}, args: {args[-1].args}, path: {args[0].path}, {args[0].operator}")
        var = func(*args,**kwargs)
        if menu.verbose:
            print(count*5*" " ,f"after: {var}-->belong to func name: {func.__name__}")
        count -= 1

        return var
    return inner