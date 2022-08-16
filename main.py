from argparse import ArgumentParser, Namespace

import yaml

import config
from components.AdditionalIntegrationManager import AdditionalIntegrationManager
from components.OptionMethodManager import OptionMethodManager


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

    return argparser.parse_args()


def set_value_to_config(args: Namespace):
    config.ENV = args.env
    config.SERVICE_NAME = args.serviceName
    config.AWS_ACCESS_KEY = args.awsAccess
    config.AWS_SECRET_ACCESS_KEY = args.awsSecret
    config.AWS_ACCESS_SESSION_TOKEN = args.awsToken


if __name__ == '__main__':
    args = get_options()
    set_value_to_config(args)

    swagger = get_input_yaml(args.input)
    optionManager = OptionMethodManager(swagger)
    swagger = optionManager.add_option_methods()
    additionalIntegrationManager = AdditionalIntegrationManager(swagger)
    swagger = additionalIntegrationManager.add_amazon_apigateway_integration()
    write_swagger(swagger, args.output)
