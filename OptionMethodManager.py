from typing import List

from SwaggerManager import SwaggerManager

default_headers = ['Content-Type', 'X-Amz-Date', 'X-Api-Key', 'X-Amz-Security-Token', 'X-Amz-User-Agent']


class OptionMethodManager(SwaggerManager):
    def __init__(self, swagger: dict):
        super().__init__(swagger)
        self.swagger: dict = swagger

    def __get_all_methods(self, path) -> List[str]:
        methods: List[str] = self.get_all_contained_service_method(path)
        methods.append('options')
        methods = [method.upper() for method in methods]
        return methods

    def __get_response(self, path: str) -> dict:
        methods: List[str] = self.__get_all_methods(path)
        headers: List[str] = default_headers
        if self.has_security(path, methods[0]):
            headers.append('Authorization')

        return {
            'description': 'common access control allows.',
            'headers': {
                'Access-Control-Allow-Headers': {
                    'schema': {
                        'type': 'string'
                    },
                    'description': ','.join(headers)
                },
                'Access-Control-Allow-Methods': {
                    'schema': {
                        'type': 'string'
                    },
                    'description': ','.join(methods)
                },
                'Access-Control-Allow-Origin': {
                    'schema': {
                        'type': 'string'
                    },
                    # fixme: get origin FQDN
                    'description': '*'
                }
            }
        }

    def add_option_methods(self) -> dict:
        path_list: List[str] = self.get_all_paths()
        for path in path_list:
            response: dict = self.__get_response(path)
            path_line = path.replace('/', '-')
            self.swagger['paths'][path]['options'] = {
                'summary': '',
                'operationId': f'options-{path_line}',
                'responses': {
                    '200': response
                },
                'description': '',
                'security': [],
                # no amazon api-gateway integrations
            }
        return self.swagger
