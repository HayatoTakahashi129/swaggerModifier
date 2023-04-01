import json
import sys

from argparse import ArgumentParser, Namespace
from collections import OrderedDict

import yaml

from configs import config
from swaggerModifier.common.ErrorHandler import show_error
from swaggerModifier.components.AdditionalIntegrationManager import AdditionalIntegrationManager
from swaggerModifier.components.OptionMethodManager import OptionMethodManager


def get_input_yaml(yaml_path: str) -> dict:
    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                         lambda loader, node: OrderedDict(loader.construct_pairs(node)))

    with open(yaml_path, 'r') as file:
        try:
            swagger_dict: dict = yaml.safe_load(file)
        except yaml.YAMLError as error:
            if hasattr(error, 'problem_mark'):
                mark = error.problem_mark
                print(f'Error position: ({mark.line + 1}:{mark.column + 1})')
            show_error('Please set valid yaml file.')
        except FileNotFoundError:
            show_error('I can NOT find input swagger file.')
        except Exception as error:
            raise error

    return swagger_dict


def write_swagger(swagger_dict: dict, yaml_path: str):
    with open(yaml_path, 'w') as file:
        if config.OUTPUT_FORMAT == 'yaml':
            yaml.safe_dump(swagger_dict, file, sort_keys=False)
        elif config.OUTPUT_FORMAT == 'json':
            json.dump(swagger_dict, file, indent=2)


def get_options():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input', type=str, required=True, help='Set input swagger file path to create.',
                           default=None)
    argparser.add_argument('-o', '--output', type=str, required=True, help='Set output file path.', default=None)
    argparser.add_argument('-e', '--env', type=str, default='dev', help='Set environment to create swagger file')
    argparser.add_argument('--serviceName', type=str, default=None,
                           help='Set service name to create swagger file. default value is retrieve from info.title '
                                'in swagger file')
    argparser.add_argument('--awsAccess', type=str, default=None,
                           help='Set AWS IAM Access Key to retrieve data from SSM parameter store.')
    argparser.add_argument('--awsSecret', type=str, default=None,
                           help='Set AWS IAM Secret Access Key to retrieve data from SSM parameter store.')
    argparser.add_argument('--awsToken', type=str, default=None,
                           help='Set AWS IAM Access Session Token to retrieve data from SSM parameter store. This is required when you IAM is using MFA.')
    argparser.add_argument('--format', type=str, default='yaml', choices=['yaml', 'json'],
                           help='Set output format as JSON or YAML.')

    return argparser.parse_args()


def set_value_to_config(args: Namespace, swagger_dict: dict):
    config.ENV = args.env
    config.SERVICE_NAME = args.serviceName
    if config.SERVICE_NAME is None:
        config.SERVICE_NAME = swagger_dict['info']['title']
    config.AWS_ACCESS_KEY = args.awsAccess
    config.AWS_SECRET_ACCESS_KEY = args.awsSecret
    config.AWS_ACCESS_SESSION_TOKEN = args.awsToken
    config.OUTPUT_FORMAT = args.format


if __name__ == '__main__':
    args = get_options()
    swagger = get_input_yaml(args.input)
    set_value_to_config(args, swagger)

    optionManager = OptionMethodManager(swagger)
    swagger = optionManager.add_option_methods()
    additionalIntegrationManager = AdditionalIntegrationManager(swagger)
    swagger = additionalIntegrationManager.add_amazon_apigateway_integration()
    write_swagger(swagger, args.output)
    print('Succeed to Create output swagger file.')
    sys.exit(0)
