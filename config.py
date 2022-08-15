from typing import Dict

import boto3

ENV: str = 'dev'
SERVICE_NAME: str = None

AWS_ACCESS_KEY: str = None
AWS_SECRET_ACCESS_KEY: str = None
AWS_ACCESS_SESSION_TOKEN: str = None

__param_cache: Dict[str, str] = {}


def __create_iam_configure() -> Dict[str, str]:
    iam_access_info: Dict[str, str] = {}
    if AWS_ACCESS_KEY is not None:
        iam_access_info['aws_access_key_id'] = AWS_ACCESS_KEY
    if AWS_SECRET_ACCESS_KEY is not None:
        iam_access_info['aws_secret_access_key'] = AWS_SECRET_ACCESS_KEY
    if AWS_ACCESS_SESSION_TOKEN is not None:
        iam_access_info['aws_session_token'] = AWS_ACCESS_SESSION_TOKEN
    return iam_access_info


def get_parameter(param: str) -> str:
    if param in __param_cache:
        return __param_cache[param]

    iam_access_info = __create_iam_configure()
    ssm = boto3.client('ssm', **iam_access_info)
    param_key: str = SERVICE_NAME + '/' + ENV + '/' + param
    response = ssm.get_parameter(Names=[param_key], WithDecryption=True)
    result = response['Parameters'][0]['Value']
    if result is None:
        raise ValueError(f'You entered unexist parameter. SERVICE=${SERVICE_NAME} ENV=${ENV} PARAM=${param}')

    __param_cache[param] = result
    return result
