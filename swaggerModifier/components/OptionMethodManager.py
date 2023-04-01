from typing import List

from configs import config
from swaggerModifier.common.SwaggerAnalyzer import SwaggerAnalyzer

DEFAULT_HEADERS = ['Content-Type', 'X-Amz-Date', 'X-Api-Key', 'X-Amz-Security-Token', 'X-Amz-User-Agent']


class OptionMethodAnalyzer(SwaggerAnalyzer):
    """
    Analyze swagger file to add options method in each api.
    """

    def __init__(self, swagger: dict):
        super().__init__(swagger)
        self.swagger: dict = swagger

    def __get_all_methods(self, path) -> List[str]:
        """
        get all allowed methods in target api.
        :param path: target api path.
        :return: allowed api methods
        """
        methods: List[str] = self.get_all_contained_service_method(path)
        methods.append('options')
        methods = [method.upper() for method in methods]
        return methods

    def __create_response(self, path: str) -> dict:
        """
        create options method response to integrate.
        :param path: target api path.
        :return: options method response information (dict format)
        """
        methods: List[str] = self.__get_all_methods(path)
        headers: List[str] = DEFAULT_HEADERS
        if self.has_security(path, self.get_all_contained_service_method(path)[0]):
            headers.append('Authorization')

        service_origin: str = config.SERVICE_ORIGIN
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
                    'description': f'{service_origin}'
                }
            }
        }

    def __get_tag(self, path: str) -> str:
        """
        get tag information from input swagger file.
        :param path: target api path
        :return: tag value
        """
        first_method: str = self.get_all_contained_service_method(path)[0]
        first_tag: str = self.get_tags(path, first_method)[0]
        return first_tag

    def add_option_methods(self) -> dict:
        """
        add option method to api with integration information that automatically response by api-gateway.
        :return: swagger file dict.
        """
        path_list: List[str] = self.get_all_paths()
        for path in path_list:
            response: dict = self.__create_response(path)
            tag: str = self.__get_tag(path)
            path_line = path.replace('/', '-')
            self.swagger['paths'][path]['options'] = {
                'summary': '',
                'operationId': f'options-{path_line}',
                'responses': {
                    '200': response
                },
                'description': '',
                'tags': [tag],
                'security': [],
                # no amazon api-gateway integrations
            }
        return self.swagger
