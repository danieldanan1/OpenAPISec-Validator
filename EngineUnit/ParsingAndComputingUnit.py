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

class ParsingAndComputingUnit:
    def __init__(self, scheme):
        self.scheme = scheme

    def parser(self):
