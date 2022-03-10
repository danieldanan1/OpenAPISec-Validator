from openapi3 import OpenAPI
import yaml


class Validation:
    def __init__(self, file_path):
        self.file_path = file_path

    def readYaml(self):
        try:
            with open(self.file_path) as f:
                spec = yaml.safe_load(f.read())
        except Exception as err:
            print(f'ERROR during reading yaml file: {err}')
        else:
            return spec

    def isValid(self):
        spec = self.readYaml()
        try:
            OpenAPI(spec)
        except Exception as err:
            print(f'ERROR yaml is not valid: {err}')