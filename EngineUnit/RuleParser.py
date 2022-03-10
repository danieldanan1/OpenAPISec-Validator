# def get_param(spec, path):
#     path_list = path.split('/')
#     response = spec
#     for element in path_list:
#         try:
#             response = response[element]
#         except Exception as err:
#             print(f'ERROR: {err}')
#             return None
#     return response
import json
class RuleParser:
    def __init__(self, rule_path):
        self.rule_path = rule_path
        self.rules = None
        self.readJson()

    def readJson(self):
        try:
            with (self.rule_path, "r") as file:
                self.rules = json.load(file)
        except Exception as err:
            print(f'ERROR during reading json file: {err}')

    def parser(self):
        print(type(self.rules))