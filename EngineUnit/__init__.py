from openapi_spec_validation import Validation
from RuleParser import RuleParser
from UserInterface import ui
import Logs

if __name__ == "__main__":
    menu = ui()
    Logs.menu = menu
    open_api = Validation(menu.api_scheme)
    is_dir = menu.rules is None
    file = menu.dir_rules if is_dir else menu.rules
    parser = RuleParser(file,is_dir)
    for rule in parser.rules:
        rule.run(open_api.spec)
        rule.run(open_api.spec)