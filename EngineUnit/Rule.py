from enums import Type,Operator
from SchemePath import PathData, SchemePath
from Logs import debug
from Report import Report

class Rule:
    """
    this class contain the definition for rule define in the rule files
    in order to start the executions of the class need to run the "run" function
    """
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
        self.__report:Report = None

        """
        the optional rule can run  
        """
        self.type_functions = {
            Type.BASE : self.runBase,
            Type.CONDITION : self.runCondition,
            Type.AND : self.runAnd,
            Type.OR : self.runOr,
            Type.ANY : self.runAny,
            Type.ALL : self.runAll
        }
        """
        the optional operation in base rule
        """
        self.operator_functions = {
            Operator.EXIST : lambda path_data: path_data is not None and ((isinstance(path_data,list)) or path_data.scheme is not None),
            Operator.NOT_EXIST :lambda path_data: path_data is None or (not (isinstance(path_data,list)) or path_data.scheme is None),
            Operator.LESS_THAN : lambda path_data : int(path_data.scheme) > int(self.value),
            Operator.GREATER_THAN : lambda path_data : int(path_data.scheme) < int(self.value),
            Operator.EQUAL :lambda path_data : path_data.scheme == self.value,
            Operator.ANY : lambda path_data :path_data.scheme in self.value,
            Operator.CONTAIN : lambda path_data : self.value in str(path_data.scheme)
        }

    def __str__(self):
        return self.type.value


    def __getPath(self, path_data:PathData):
        """
        calculate the path of self.path
        :param path_data: contain the current scheme and the current args
        :return: PathData | list[PathData] or None
        if the path point to list return list[PathData]
        if the path point to specific element return PathData
        else if the epath not exist return None
        """
        return SchemePath(self.path).getPath(self.__root_scheme, path_data.args)


    def run(self, scheme:dict):
        """
        start run the validation
        :param scheme: dict the root open api scheme
        :return: void
        """
        report = Report()
        self.__run(PathData(scheme, {}), scheme,report)
        report.createReport()



    def __run(self, path_data: PathData, root_schema,report:Report):
        """
         run specific rule depending on the self.type
        :param path_data: PathData contain the current scheme and the current args
        :param root_schema: dict the root open api scheme
        :param report: Report the report object
        :return: bool if the current rule finished successfully
        """
        self.__root_scheme = root_schema
        self.__report = report
        runRule = self.type_functions.get(self.type, self.typeNotExist)
        try:
            is_success = runRule(path_data)
        except Exception as err:
            #raise err
            print(err)
            is_success = False
        self.printMessage(is_success, path_data)
        return is_success

    #@debug
    def printMessage(self, is_success, path_data: PathData):
        """
        handles the messages if user defined in the rule files
        :param is_success: bool if need to print the success message or the fail message
        :param path_data: PathData contain the current scheme and the current args
        :return: void
        """
        message = None
        msg_dict = {}
        if is_success and self.success_msg:
            message = self.success_msg
        elif not is_success and self.fail_msg:
            message = self.fail_msg
        if message is not None:
            path:str = self.path
            if path is not None:
                for key,value in path_data.args.items():
                    path = path.replace(f'${key}',value)
            self.__report.addToReport(message,path)

    @debug
    def runBase(self, path_data: PathData):
        pathsData = self.__getPath(path_data)
        return self.operator_functions[self.operator](pathsData)

    @debug
    def runCondition(self, path_data: PathData):
        condition_result = self.rule.__run(path_data, self.__root_scheme,self.__report)
        if condition_result and (self.rtrue is not None):
            return self.rtrue.__run(path_data, self.__root_scheme,self.__report)
        if (not condition_result) and (self.rfalse is not None):
            return self.rfalse.__run(path_data, self.__root_scheme,self.__report)

    @debug
    def runAnd(self, path_data: PathData):
        return all([r.__run(path_data, self.__root_scheme,self.__report) for r in self.rule])

    @debug
    def runOr(self, path_data: PathData):
        return any([r.__run(path_data, self.__root_scheme,self.__report) for r in self.rule])

    @debug
    def runAny(self, path_data: PathData):
        pathsData:list[PathData] = self.__getPath(path_data)
        if pathsData is not None:
            return any([self.rule.__run(data, self.__root_scheme,self.__report) for data in pathsData])
        else:
            return False

    @debug
    def runAll(self, path_data: PathData):
        pathsData:list[PathData] = self.__getPath(path_data)
        if pathsData is not None:
            return all([self.rule.__run(data, self.__root_scheme,self.__report) for data in pathsData])
        else:
            return False



    @debug
    def typeNotExist(self, pathData:PathData):
        raise 'typeNotExist'



