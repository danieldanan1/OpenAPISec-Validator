from enums import Type,Operator
from SchemePath import PathData, SchemePath
count = 0
def debug(func):

    def inner(*args,**kwargs):
        global count
        count+=1
        # print(count*" " ,f"before: {func.__name__}, args: {args[-1].args}, path: {args[0].path}")
        var = func(*args,**kwargs)
        # print(count*" " ,f"after: {var}-->belong to func name: {func.__name__}")
        count -= 1

        return var
    return inner

class Rule:

    def __init__(self):
        self.type = None
        self.rtrue = None
        self.rfalse = None
        self.path = None
        self.rule = None
        self.operator = None
        self.value = None
        self.fail_msg = None
        self.success_msg = None
        self.__root_scheme = None

        self.type_functions = {
            Type.BASE : self.runBase,
            Type.CONDITION : self.runCondition,
            Type.AND : self.runAnd,
            Type.OR : self.runOr,
            Type.ANY : self.runAny,
            Type.ALL : self.runAll
        }

        self.operator_functions = {
            Operator.EXIST : lambda path_data: self.getPath(path_data) is not None,
            Operator.NOT_EXIST :lambda path_data: self.getPath(path_data) is None,
            Operator.LESS_THAN : lambda path_data : int(path_data.scheme) > int(self.value),
            Operator.GREATER_THAN : lambda path_data : int(path_data.scheme) < int(self.value),
            Operator.EQUAL :lambda path_data : int(path_data.scheme) == int(self.value),
            Operator.ANY : lambda path_data :self.value in path_data.scheme,
            Operator.CONTAIN : lambda path_data : self.value in self.getPath(path_data)
        }

    def __str__(self):
        return self.type.value

    def getPath(self, path_data:PathData):
        return SchemePath(self.path).getPath(self.__root_scheme, path_data.args)


    def run(self, scheme:dict):
        self.__run(PathData(scheme, {}), scheme)



    def __run(self, path_data: PathData, root_schema):
        self.__root_scheme = root_schema
        runRule = self.type_functions.get(self.type, self.typeNotExist)
        is_success = runRule(path_data)
        self.printMessage(is_success, path_data)
        return is_success

    @debug
    def printMessage(self, is_success, path_data: PathData):
        message = None
        if is_success:
            if self.success_msg:
                message = self.success_msg
        else:
            if self.fail_msg:
                message = self.fail_msg
        if message is not None:
            print(is_success, self.type, self.path, path_data.args, message)

    @debug
    def runBase(self, path_data: PathData):
        return self.operator_functions[self.operator](path_data)

    @debug
    def runCondition(self, path_data: PathData):
        condition_result = self.rule.__run(path_data, self.__root_scheme)
        if condition_result and (self.rtrue is not None):
            return self.rtrue.__run(path_data, self.__root_scheme)
        if (not condition_result) and (self.rfalse is not None):
            return self.rfalse.__run(path_data, self.__root_scheme)

    @debug
    def runAnd(self, path_data: PathData):
        return all(r.__run(path_data, self.__root_scheme) for r in self.rule)

    @debug
    def runOr(self, path_data: PathData):
        return any(r.__run(path_data, self.__root_scheme) for r in self.rule)

    @debug
    def runAny(self, path_data: PathData):
        pathsData:list[PathData] = self.getPath(path_data)
        return any(self.rule.__run(data, self.__root_scheme) for data in pathsData)

    @debug
    def runAll(self, path_data: PathData):
        paths_data:list[PathData] = self.getPath(path_data)
        return all(self.rule.__run(data, self.__root_scheme) for data in paths_data)



    @debug
    def typeNotExist(self, pathData:PathData):
        raise 'typeNotExist'



