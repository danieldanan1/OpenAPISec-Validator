import enum


class Type(enum.Enum):
    BASE = "basse"
    CONDITION = "condition"
    AND = "and"
    OR = "or"
    ANY = "any"
    ALL = "all"

    # def __str__(self):
    #     return ', '.join(item.value for item in Type)


class Operator(enum.Enum):
    EXIST = "exist"
    NOT_EXIST = "not_exist"
    LESS_THAN = "lt"
    GREATER_THAN = "gt"
    EQUAL = "eq"
    ANY = "any"
    CONTAIN = "contain"

    # def __str__(self):
    #     return ', '.join(item.value for item in Operator)


class MessageType(enum.Enum):
    SUCCESS_MSG = "success_msg"
    FAIL_MSG = "fail_msg"

    # def __str__(self):
    #     return ', '.join(item.value for item in MessageType)