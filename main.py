from argparse import ArgumentParser

import yaml

import config
from AdditionalIntegrationManager import AdditionalIntegrationManager
from OptionMethodManager import OptionMethodManager


def get_input_yaml(yaml_path: str) -> dict:
    with open(yaml_path, 'r') as file:
        try:
            swagger_dict: dict = yaml.safe_load(file)
        except yaml.YAMLError as error:
            print(error)
            raise error
    return swagger_dict


def write_swagger(swagger_dict: dict, yaml_path: str):
    with open(yaml_path, 'w') as file:
        yaml.dump(swagger_dict, file)


def get_options():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input', type=str, required=True, help='Set input swagger file path to create.')
    argparser.add_argument('-o', '--output', type=str, required=True, help='Set output file path.')
    argparser.add_argument('-e', '--env', type=str, default='dev', help='Set environment to create swagger file')
    return argparser.parse_args()


if __name__ == '__main__':
    args = get_options()
    config.ENV = args.env
    swagger = get_input_yaml(args.input)
    optionManager = OptionMethodManager(swagger)
    swagger = optionManager.add_option_methods()
    additionalIntegrationManager = AdditionalIntegrationManager(swagger)
    swagger = additionalIntegrationManager.add_amazon_apigateway_integration()
    write_swagger(swagger, args.output)
