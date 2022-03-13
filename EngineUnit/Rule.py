from enums import Type,Operator


class PathData:
    def __init__(self,scheme:dict,args:dict):
        self.scheme:dict = scheme
        self.args:dict = args
    def __str__(self):
        return f"{self.scheme},{self.args}"

class SchemePath:
    def __init__(self, path:str):
        self.path = path
        self.__result =[]



    #TODO relative Path in the scheme
    def getPath(self, scheme: dict, args:dict={}):
        self.__result = []
        path_items = self.path.split(".")
        self.__getPathRec(path_items, scheme, args)#TODO handle errors
        return self.__result

    def __getPathRec(self, path: list, scheme: dict, args:dict={}):
        while(len(path) > 0):
            if type(scheme) == list:
                for sub_scheme in scheme:
                    sub_path = path.copy()
                    self.__getPathRec(sub_path,sub_scheme,args)
                return
            item:str = path.pop(0)
            if(item.startswith("#")):#var Defenishion
                var = item[1:]
                for item in scheme.keys():
                    sub_path = path.copy()
                    sub_args = args.copy()
                    sub_args[var] = item
                    self.__getPathRec(sub_path,scheme[item],sub_args)
                return
            if(item.startswith("$")):#var Value
                item = args[item[1:]]#TODO raise if not found
            if(item in scheme):
                scheme = scheme[item]#TODO test case when raise error if all paths not found
            else:
                return
        if(type(scheme) == list):
            for item in scheme:
                self.__result.append(PathData(item, args))
        else:
            self.__result.append(PathData(scheme, args))

    # def getPathRec1(self,path: list, scheme: dict, args={}):
    #     sub_path = path.copy()
    #     if (len(path) == 0):
    #         return
    #     item = sub_path.pop(0)
    #     if "{" in item:
    #         var = item[1:-1]
    #         for sub_item in scheme.keys():
    #             item_args = args.copy()
    #             item_args[var] = sub_item
    #             self.getPathRec1(sub_path, scheme[sub_item], item_args)
    #     else:
    #         if item in scheme:
    #             pass
    #         else:
    #             raise "path not exist"


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

        self.type_functions = {
            Type.BASE : self.runBase,
            Type.CONDITION : self.runCondition,
            Type.AND : self.runAnd,
            Type.OR : self.runOr,
            Type.ANY : self.runAny,
            Type.ALL : self.runAll
        }


        self.operator_functions = {
            Operator.EXIST : lambda pathData: self.getPath(pathData) != [],
            Operator.NOT_EXIST :lambda pathData: self.getPath(pathData)  == [],
            Operator.LESS_THAN : lambda pathData : pathData.scheme>self.value,
            Operator.GREATER_THAN : lambda pathData : pathData.scheme<self.value,
            Operator.EQUAL :lambda pathData : pathData.scheme == self.value,
            Operator.ANY : lambda pathData :self.value in pathData.scheme,
            Operator.CONTAIN : lambda pathData : self.value in self.getPath(pathData)
        }


    def __str__(self):
        return self.type.value


    def getPath(self, pathData:PathData):
        schemePath = SchemePath(self.path)
        results = schemePath.getPath(pathData.scheme, pathData.args)
        return results[0] if len(results) == 1 else results

    def run(self,scheme:dict):
        self.__run(PathData(scheme, {}))

    def __run(self, pathData:PathData):
        runRule = self.type_functions.get(self.type,self.typeNotExist)
        is_success = runRule(pathData)
        self.printMessage(is_success,pathData)
        return is_success

    def printMessage(self,is_success,pathData:PathData):
        message = None
        if is_success:
            if self.success_msg:
                message = self.success_msg
        else:
            if self.fail_msg:
                message = self.fail_msg
        if message is not None:
            print(is_success,self.type, self.path,pathData.args,message)


    def runBase(self,pathData:PathData):
        return self.operator_functions[self.operator](pathData)

    def runCondition(self,pathData:PathData):
        condition_result = self.rule.__run(pathData)
        if condition_result and (self.rtrue is not None):
            return self.rtrue.__run(pathData)
        if (not condition_result) and (self.rfalse is not None):
            return self.rfalse.__run(pathData)



    def runAnd(self,pathData:PathData):
        return all(r.__run(pathData) for r in self.rule)

    def runOr(self,pathData:PathData):
        return any(r.__run(pathData) for r in self.rule)

    def runAny(self,pathData:PathData):
        pathsData:list[PathData] = self.getPath(pathData)
        return any(self.rule.__run(data) for data in pathsData)

    def runAll(self,pathData:PathData):
        pathsData:list[PathData] = self.getPath(pathData)
        return all(self.rule.__run(data) for data in pathsData)
    def typeNotExist(self,pathData:PathData):
        raise 'typeNotExist'

