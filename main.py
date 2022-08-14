from argparse import ArgumentParser

import yaml

import config


def get_input_yaml(yaml_path: str) -> dict:
    with open(yaml_path, 'r') as file:
        try:
            swagger_dict: dict = yaml.safe_load(file)
        except yaml.YAMLError as error:
            print(error)
            raise error
    return swagger_dict


def get_options():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input', type=str, help='Set input swagger file path to create.')
    argparser.add_argument('-o', '--output', type=str, help='Set output file path.')
    argparser.add_argument('-e''--env', type=str, default='dev', help='Set environment to create swagger file')
    return argparser.parse_args()


if __name__ == '__main__':
    args = get_options()
    config.ENV = args.env
    swagger = get_input_yaml(args.input)
