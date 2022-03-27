import enum

"""
list of the optional rule
"""
class Type(enum.Enum):
    BASE = "basse"
    CONDITION = "condition"
    AND = "and"
    OR = "or"
    ANY = "any"
    ALL = "all"

"""
list of the optional operator in base rule
"""
class Operator(enum.Enum):
    EXIST = "exist"
    NOT_EXIST = "not_exist"
    LESS_THAN = "lt"
    GREATER_THAN = "gt"
    EQUAL = "eq"
    ANY = "any"
    CONTAIN = "contain"


"""
list of the optional messages
"""
class MessageType(enum.Enum):
    SUCCESS_MSG = "success_msg"
    FAIL_MSG = "fail_msg"
