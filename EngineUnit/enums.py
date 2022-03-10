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