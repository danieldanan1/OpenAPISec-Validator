
class Rule:

    def __init__(self):
        self.type = None
        self.rtrue = None
        self.rfalse = None
        self.path = None
        self.rule =None
        self.value = None
        self.error_msg = None
        self.success_msg = None










rule_class:
{
    type: "type"
    true: "rule"/o
    false: "rule"/o
    path: "path"
    rule: "rule | base_rule"/o
    value: "string | int | list"
    error_mesege: "string"
    secsses_msg: "string"
}