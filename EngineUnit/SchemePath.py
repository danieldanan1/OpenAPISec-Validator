class PathData:
    def __init__(self, scheme: dict, args: dict):
        self.scheme: dict = scheme
        self.args: dict = args

    def __str__(self):
        return f"{self.scheme},{self.args}"


class SchemePath:
    def __init__(self, path:str):
        self.path = path
        self.__result =[]
        self.__result_is_list = False
        self.__result_is_value = False
    #TODO relative Path in the scheme
    def getPath(self, scheme: dict, args:dict={}):
        self.__result = []
        if(self.path.endswith('%')):
            self.__result_is_value = True
            self.path = self.path[:-1]
        path_items = self.path.split(".")
        self.__getPathRec(path_items, scheme, args)#TODO handle errors
        if len(self.__result) > 0:
            return self.__result if self.__result_is_list else self.__result[0]
        return None

    def __getPathRec(self, path: list, scheme: dict, args:dict={}):
        while len(path) > 0:
            if scheme is None:
                return
            if isinstance(scheme,list):
                for sub_scheme in scheme:
                    sub_path = path.copy()
                    self.__result_is_list = True
                    self.__getPathRec(sub_path,sub_scheme,args)
                return
            item:str = path.pop(0)
            if isinstance(scheme,str) and len(path) == 0  and item.startswith("#"):
                sub_args = args.copy()
                sub_args[item[1:]] = scheme
                self.__result.append(PathData(None, sub_args))
                return

            if(item.startswith("#")):#variable definition
                var = item[1:]
                for item in scheme.keys():
                    sub_path = path.copy()
                    sub_args = args.copy()
                    sub_args[var] = item
                    self.__result_is_list = True
                    self.__getPathRec(sub_path,scheme[item],sub_args)
                return

            if(item.startswith("$")):#var Value
                item = args[item[1:]]

            if(item in scheme):
                scheme = scheme[item]
            else:
                return

        if(isinstance(scheme,list) and not self.__result_is_value):
            self.__result_is_list = True
            for item in scheme:
                self.__result.append(PathData(item, args))
        else:
            self.__result.append(PathData(scheme, args))