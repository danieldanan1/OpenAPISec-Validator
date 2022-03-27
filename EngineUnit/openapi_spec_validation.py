from openapi3 import OpenAPI
import yaml


class Validation:
    """
    read and validate the open api scheme
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.spec = None
        self.readYaml()

    def readYaml(self):
        """
        read and parse the open api scheme and savaed in self.spec
        :return: void
        """
        try:
            with open(self.file_path) as f:
                self.spec = yaml.safe_load(f.read())
        except Exception as err:
            print(f'ERROR during reading yaml file: {err}')
            raise err

    def isValid(self):
        """
        check if the open api scheme in valid
        :return: bool
        """
        try:
            OpenAPI(self.spec)
        except Exception as err:
            print(f'ERROR yaml is not valid: {err}')
            return False
        else:
            return True




