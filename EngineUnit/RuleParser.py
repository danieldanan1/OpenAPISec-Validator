import json
from enums import Type, Operator, MessageType
from Rule import Rule


class RuleParser:
    def __init__(self, rule_path):
        self.rule_path = rule_path
        self.__operators_should_contain_value = [Operator.LESS_THAN, Operator.GREATER_THAN, Operator.EQUAL,
                                                 Operator.ANY, Operator.CONTAIN]
        self.rule_scheme = None
        self.rules = []
        self.readJson()

    def readJson(self):
        try:
            with open(self.rule_path) as file:
                self.rule_scheme = json.load(file)
        except Exception as err:
            print(f'ERROR during reading json file: {err}')

    def callingToParser(self):
        if "rules" in self.rule_scheme:
            for ruleScheme in self.rule_scheme["rules"]:
                self.rules.append(self.parser(ruleScheme))
        else:
            self.rules.append(self.parser(self.rule_scheme))

    def parser(self, ruleScheme):
        rule:Rule
        type_dict = {Type.BASE: self.parseBase,
                     Type.ALL: self.parseAll,
                     Type.ANY: self.parseAny,
        }
        if type(ruleScheme) is str:
            rule = self.parseBase(ruleScheme)
        else:
            op = set(ruleScheme.keys()).intersection({element.value for element in Type})
            if len(op) == 1:
                operator = op.pop()
                rule = type_dict[operator](ruleScheme);
            else:
                raise "ERROR in Parser method there is more than or less than one operator"
        return rule


    def parseBase(self, ruleScheme):
        rule_elements = ruleScheme.split(",")
        rule_elements_size = len(rule_elements)-2
        rule_obj = Rule()
        rule_obj.type = Type.BASE
        rule_obj.path = rule_elements[0]
        rule_obj.operator = Operator(rule_elements[1])
        if (rule_elements_size > 0) and (rule_elements[2] in self.__operators_should_contain_value):
            rule_obj.value = rule_elements[2]
            rule_elements_size -= 1
        for i in range(1,rule_elements_size+1):
            msg_type, msg_content = rule_elements[-i].split("=")
            match msg_type:
                case MessageType.SUCCESS:
                    rule_obj.success_msg = MessageType.SUCCESS,
                case MessageType.FAIL:
                    rule_obj.fail_msg = MessageType.FAIL,
                case _:
                    raise f"message type is not exist\nPlease use one of this types: {MessageType}"
        return rule_obj


    def parseCondition(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.CONDITION
        rule_obj.rule = self.parser(ruleScheme[Type.CONDITION])
        if "true" in ruleScheme:
            rule_obj.rtrue = self.parser(ruleScheme["true"])
        if "false" in ruleScheme:
            rule_obj.rfalse = self.parser(ruleScheme["false"])
        self.messages(ruleScheme, rule_obj)
        return rule_obj


    def parseAnd(self, ruleScheme:dict):
        rule_obj = Rule()
        rule_obj.rule = [self.parser(item) for item in ruleScheme[Type.AND]]
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseOr(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.rule = [self.parser(item) for item in ruleScheme[Type.OR]]
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseAny(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.ANY
        rule_obj.path = ruleScheme[rule_obj.type]
        if "rule" in ruleScheme:
            rule_obj.rule = self.parser(ruleScheme["rule"])
        else:
            raise "rule label is not defined under ANY label"
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def parseAll(self, ruleScheme):
        rule_obj = Rule()
        rule_obj.type = Type.ALL
        rule_obj.path = ruleScheme[rule_obj.type]
        if "rule" in ruleScheme:
            rule_obj.rule = self.parser(ruleScheme["rule"])
        else:
            raise "rule label is not defined under ALL label"
        self.messages(ruleScheme, rule_obj)
        return rule_obj

    def messages(self, ruleScheme, rule_obj):
        if MessageType.SUCCESS_MSG in ruleScheme:
            rule_obj.success_msg = ruleScheme[MessageType.SUCCESS_MSG]
        if MessageType.FAIL_MSG in ruleScheme:
            rule_obj.fail_msg = ruleScheme[MessageType.FAIL_MSG]

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