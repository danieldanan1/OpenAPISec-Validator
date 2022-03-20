from openapi3 import OpenAPI
import yaml
from userInterface import ui
from Rule import PathData,SchemePath,Rule
from RuleParser import RuleParser

class Validation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.spec = None
        self.readYaml()

    def readYaml(self):
        try:
            with open(self.file_path) as f:
                self.spec = yaml.safe_load(f.read())
        except Exception as err:
            print(f'ERROR during reading yaml file: {err}')

    def isValid(self):
        try:
            OpenAPI(self.spec)
        except Exception as err:
            print(f'ERROR yaml is not valid: {err}')
            return False
        else:
            return True

if __name__ == "__main__":
    menu = ui()
    # open_api =Validation(r"C:\Users\shahor\PycharmProjects\OpenAPISec-Validator\Rules\exampleYaml.yaml")
    # Parser = RuleParser(r"F:\Users\User\Downloads\exampel.json")
    #
    # Parser.callingToParser()
    # for rule in Parser.rules:
    #     rule.run(open_api.spec)


#print(a.spec,type(a.spec))
#schemePath = SchemePath("paths./configuration/michael.get.parameters.schema")
# schemePath = SchemePath("paths.#path.post.operationId")
#
# results = schemePath.getPath(open_api.spec, {})
# print(*results,sep ="\n")


