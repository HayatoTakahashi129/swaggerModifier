import json
import os
import sys
from argparse import ArgumentParser, Namespace
from collections import OrderedDict

import yaml

from swaggerModifier.common.ErrorHandler import show_error
from swaggerModifier.components.AdditionalIntegrationManager import AdditionalIntegrationAnalyzer
from swaggerModifier.components.OptionMethodManager import OptionMethodAnalyzer
from swaggerModifier.configs import config


def get_input_yaml(yaml_path: str) -> dict:
    """
    parse yaml file
    :param yaml_path: input path for open api yaml file.
    :return: parsed open-api information (dict format)
    """
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


def write_swagger(swagger_dict: dict, yaml_path: str) -> None:
    """
    create or overwrite yaml file.
    :param swagger_dict: swagger object to write
    :param yaml_path: output yaml file path
    """
    yaml_path_list = yaml_path.split('/')
    os.makedirs(os.path.join(*yaml_path_list[:-1]), exist_ok=True)
    with open(yaml_path, 'w') as file:
        if config.OUTPUT_FORMAT == 'yaml':
            yaml.safe_dump(swagger_dict, file, sort_keys=False)
        elif config.OUTPUT_FORMAT == 'json':
            json.dump(swagger_dict, file, indent=2)


def get_options() -> Namespace:
    """
    parse options in command.
    :return: parsed argument result.
    """
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input', type=str, required=True, help='Set input swagger file path to create.',
                           default=None)
    argparser.add_argument('-o', '--output', type=str, required=True, help='Set output file path.', default=None)
    argparser.add_argument('-e', '--env', type=str, default='dev', help='Set environment to create swagger file')
    argparser.add_argument('--serviceName', type=str, default=None,
                           help='Set service name to create swagger file. default value is retrieve from info.title '
                                'in swagger file')
    argparser.add_argument('--origin', type=str, default=None, help='Set service origin domain for api.')
    argparser.add_argument('--cognitoPoolId', type=str, default=None,
                           help='Set cognito user pool id for security check in api-gateway.')
    argparser.add_argument('--format', type=str, default='yaml', choices=['yaml', 'json'],
                           help='Set output format as JSON or YAML.')

    return argparser.parse_args()


def set_value_to_config(args: Namespace, swagger_dict: dict) -> None:
    """
    set config value from arguments.
    :param args: option get from command
    :param swagger_dict: input swagger file parsed object
    """
    config.ENV = args.env
    config.SERVICE_NAME = args.serviceName
    if config.SERVICE_NAME is None:
        config.SERVICE_NAME = swagger_dict['info']['title']
    config.SERVICE_ORIGIN = args.origin
    config.COGNITO_USERPOOL_ID = args.cognitoPoolId
    config.OUTPUT_FORMAT = args.format


if __name__ == '__main__':
    args = get_options()
    swagger = get_input_yaml(args.input)
    set_value_to_config(args, swagger)

    optionManager = OptionMethodAnalyzer(swagger)
    swagger = optionManager.add_option_methods()
    additionalIntegrationManager = AdditionalIntegrationAnalyzer(swagger)
    swagger = additionalIntegrationManager.add_amazon_apigateway_integration()
    write_swagger(swagger, args.output)
    print('Succeed to Create output swagger file.')
    sys.exit(0)
