import json
from enums import Type, Operator, MessageType
from Rule import Rule
from glob import glob


class RuleParser:
    """
    the class parse the rule files and return list of Rules
    """
    def __init__(self, rule_path,is_dir:bool = True):
        """

        :param rule_path: str the path to rule file
        :param is_dir: bool indication if the path is dir or a file
        """
        self.rule_path = rule_path
        self.__operators_should_contain_value = [Operator.LESS_THAN.value, Operator.GREATER_THAN.value, Operator.EQUAL.value,
                                                 Operator.ANY.value, Operator.CONTAIN.value]
        self.rule_scheme = None
        self.rules = []
        self.is_dir = is_dir
        self.type_dict = {Type.BASE: self.parseBase,
                          Type.ALL: self.parseAll,
                          Type.ANY: self.parseAny,
                          Type.AND: self.parseAnd,
                          Type.OR: self.parseOr,
                          Type.CONDITION: self.parseCondition
                         }
        if self.is_dir:
            self.readJsonDir()
        else:
            self.readJson(self.rule_path)


    def readJson(self,path):
        """
        read rule file and run the parser
        :param path: str the file path
        :return: void
        """
        try:
            with open(path) as file:
                self.rule_scheme = json.load(file)
            self.callingToParser()
        except Exception as err:
            print(f'ERROR during reading json file: {err}')
            raise err

    def readJsonDir(self):
        """
        read folder of rules files
        :return:
        """
        for path in glob(self.rule_path+"/*.json"):
            self.readJson(path)

    def callingToParser(self):
        """
        start the parsing process and save the result in self.rules
        :return: void
        """
        if "rules" in self.rule_scheme:
            for ruleScheme in self.rule_scheme["rules"]:
                self.rules.append(self.parser(ruleScheme))
        else:
            self.rules.append(self.parser(self.rule_scheme))

    def parser(self, ruleScheme):
        """
        parse specific rule in the file
        :param ruleScheme: dict the current rule scheme the parser run
        :return: Rule the function parse
        """
        rule:Rule

        if type(ruleScheme) is str:
            rule = self.parseBase(ruleScheme)
        else:
            op = set(ruleScheme.keys()).intersection({element.value for element in Type})
            if len(op) == 1:
                operator = op.pop()
                parserFunc = self.type_dict[Type(operator)]
                rule = parserFunc(ruleScheme);
            else:
                raise "ERROR in Parser method there is more than or less than one operator"
        return rule


    def parseBase(self, ruleScheme):
        rule_elements = self.ruleSplit(ruleScheme)
        rule_elements_size = len(rule_elements)-2
        rule_obj = Rule()
        rule_obj.type = Type.BASE
        rule_obj.path = rule_elements[0]
        rule_obj.operator = Operator(rule_elements[1])
        if (rule_elements_size > 0) and (rule_elements[1] in self.__operators_should_contain_value):
            rule_obj.value = rule_elements[2]
            rule_elements_size -= 1
        #print(rule_obj.type)
        for i in range(1,rule_elements_size+1):
            msg_type, msg_content = rule_elements[-i].split("=")
            # print(msg_type, msg_content,type(msg_type), type(msg_content),rule_elements[-i],type(rule_elements[-i]))
            match msg_type:
                case MessageType.SUCCESS_MSG.value:
                    rule_obj.success_msg = msg_content
                case MessageType.FAIL_MSG.value:
                    rule_obj.fail_msg = msg_content
                case _:
                    raise f"message type is not exist\nPlease use one of this types: {','.join(i.value for i in MessageType)}"
        return rule_obj

    def ruleSplit(self,data,delimiter:str = ',',start:str ='[' ,end:str = ']'):
        """
        split the base rule to element
        :param data: str contain the row data of the base rule
        :param delimiter: str the delimiter for separate between the element
        :param start: the starting char of list defenestration if exist
        :param end: the ending char of list defenestration if exist
        :return: list containing the element of the base rule
        """
        in_range = False
        result = []
        element = ""
        for char in data:
            if char == delimiter and not in_range:
                result.append(element)
                element = ""
            elif char == start:
                in_range = True
            elif char == end:
                in_range = False
                element = element.split(delimiter)
            else:
                element += char
        result.append(element)
        return result

    def parseCondition(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.CONDITION
        rule_obj.rule = self.parser(ruleScheme[Type.CONDITION.value])
        if "true" in ruleScheme:
            rule_obj.rtrue = self.parser(ruleScheme["true"])
        if "false" in ruleScheme:
            rule_obj.rfalse = self.parser(ruleScheme["false"])
        self.messages(ruleScheme, rule_obj)
        return rule_obj


    def parseAnd(self, ruleScheme:dict):
        rule_obj = Rule()
        rule_obj.type = Type.AND
        rule_obj.rule = [self.parser(item) for item in ruleScheme[Type.AND.value]]
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseOr(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.OR
        rule_obj.rule = [self.parser(item) for item in ruleScheme[Type.OR.value]]
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseAny(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.ANY
        rule_obj.path = ruleScheme[rule_obj.type.value]
        if "rule" in ruleScheme:
            rule_obj.rule = self.parser(ruleScheme["rule"])
        else:
            raise "rule label is not defined under ANY label"
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseAll(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.ALL
        rule_obj.path = ruleScheme[rule_obj.type.value]
        if "rule" in ruleScheme:
            rule_obj.rule = self.parser(ruleScheme["rule"])
        else:
            raise "rule label is not defined under ALL label"
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def messages(self, ruleScheme, rule_obj):
        if MessageType.SUCCESS_MSG.value in ruleScheme:
            rule_obj.success_msg = ruleScheme[MessageType.SUCCESS_MSG.value]
        if MessageType.FAIL_MSG.value in ruleScheme:
            rule_obj.fail_msg = ruleScheme[MessageType.FAIL_MSG.value]




#TODO: can give us an indicate of error location in the yaml file
# import yaml
# from yaml.loader import SafeLoader
#
# class SafeLineLoader(SafeLoader):
#     def construct_mapping(self, node, deep=False):
#         mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
#         # Add 1 so line numbering starts at 1
#         mapping['__line__'] = node.start_mark.line + 1
#         return mapping
#
# with open('/Users/daniel/OpenAPISec-Validator/Rules/exampleYaml.yaml') as f:
#     data = yaml.load(f, Loader=SafeLineLoader)
#     print(data)