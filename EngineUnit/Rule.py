import enum

class Type(enum.Enum):
    BASE = "basse"
    IF = "if"
    IF_ELSE = "if_else"
    AND = "and"
    OR = "or"
    ANY = "any"
    ALL = "all"

class Operator(enum.Enum):
    EXIST = "exist"
    NOT_EXIST = "not_exist"
    LESS_THAN = "lt"
    GREATER_THAN = "gt"
    EQUAL = "eq"
    ANY = "any"
    CONTAIN = "contain"

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
