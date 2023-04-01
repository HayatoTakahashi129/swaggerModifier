from typing import List

from configs import config
from swaggerModifier.common.ErrorHandler import show_error
from swaggerModifier.common.SwaggerManager import SwaggerManager

security_schema_name = 'ID-Token'


def get_security_integration() -> dict:
    cognito_id = config.get_parameter('COGNITO_USERPOOL_ID2')
    return {
        'x-amazon-apigateway-authtype': 'cognito_user_pools',
        'x-amazon-apigateway-authorizer': {
            'type': 'cognito_user_pools',
            'providerARNs': [
                'arn:aws:cognito-idp:${AWS::Region}:${AWS::AccountId}:userpool/${AWS::Region}_{cognito}'.replace(
                    '{cognito}', cognito_id)
            ],
            'identityValidationExpression': '.*'
        }
    }


default_headers = ['Content-Type', 'X-Amz-Date', 'X-Api-Key', 'X-Amz-Security-Token']


class AdditionalIntegrationManager(SwaggerManager):
    def __init__(self, swagger: dict):
        super().__init__(swagger)
        self.swagger: dict = swagger

    def __get_all_methods(self, path: str):
        methods: List[str] = self.get_all_contained_service_method(path)
        methods.append('options')
        methods = [method.upper() for method in methods]
        return methods

    def __get_option_integration(self, path: str) -> dict:
        methods: List[str] = self.__get_all_methods(path)
        headers = default_headers
        if self.has_security(path, self.get_all_contained_service_method(path)[0]):
            headers.append('Authorization')
        service_origin = config.get_parameter('SERVICE_ORIGIN')
        return {
            'x-amazon-apigateway-integration': {
                'responses': {
                    'default': {
                        'statusCode': '200',
                        'responseParameters': {
                            'method.response.header.Access-Control-Allow-Headers': "'{headers}'".format(
                                headers=','.join(headers)),
                            'method.response.header.Access-Control-Allow-Methods': "'{methods}'".format(
                                methods=','.join(methods)),
                            'method.response.header.Access-Control-Allow-Origin': f"'{service_origin}'"
                        },
                        'responseTemplates': {
                            'application/json': '{}'
                        }
                    }
                },
                'requestTemplates': {
                    'application/json': '{"statusCode": 200}'
                },
                'passthroughBehavior': 'when_no_match',
                'type': 'mock'
            }
        }

    def __add_integration_to_option_method(self, path: str):
        option_integration: dict = self.__get_option_integration(path)
        self.swagger['paths'][path]['options'].update(option_integration)

    def __get_lambda_name(self, path: str, method: str) -> str:
        tags: List[str] = self.get_tags(path, method)
        # use first set tags. fixme: change to use tag which is define as service tag.
        service_tag: str = tags[0]
        service_name: str = config.SERVICE_NAME
        return service_name + 'Api' + service_tag + '-' + config.ENV  # amplify can only enter alphanumeric.

    def __add_integration_to_service_method(self, path: str):
        methods: List[str] = self.get_all_contained_service_method(path)
        for method in methods:
            lambda_name: str = self.__get_lambda_name(path, method)
            self.swagger['paths'][path][method].update({
                'x-amazon-apigateway-integration': {
                    'uri': 'arn:${AWS::Partition}:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:{lambdaName}/invocations'.replace(
                        '{lambdaName}', lambda_name),
                    'passthroughBehavior': 'when_no_templates',
                    'httpMethod': 'POST',
                    'type': 'aws_proxy'
                }
            })

    # add integration for lambda

    def __add_security_integration(self):
        if security_schema_name not in self.swagger['components']['securitySchemas']:
            show_error(f'Please set {security_schema_name} in `components.securitySchemas` in input swagger file.')
        security_integration: dict = get_security_integration()
        self.swagger['components']['securitySchemes'][security_schema_name].update(security_integration)

    def add_amazon_apigateway_integration(self) -> dict:
        if 'securitySchemas' in self.swagger['components']:
            if security_schema_name in self.swagger['components']['securitySchemas']:
                self.__add_security_integration()

        path_list: List[str] = self.get_all_paths()
        for path in path_list:
            self.__add_integration_to_option_method(path)
            self.__add_integration_to_service_method(path)

        return self.swagger
