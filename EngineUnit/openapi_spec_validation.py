from openapi3 import OpenAPI
import yaml


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




