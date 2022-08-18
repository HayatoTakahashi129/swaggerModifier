# Amplify API-Gateway Swagger Modifier

## Overview

This project is to create swagger file that can import to AWS API-GATEWAY.  
You need to add integrations to swagger yaml file like `x-amazon-apigateway-integration` but this project will
automatically create for you. And also this project will create OPTIONS method to swagger file automatically.  
This project assumes API-GATEWAY and Lambda configuration.

## Variable Descriptions

There are a few variables in this README.

* `${serviceName}` is a variable set by `info.title` in swagger.
* `${tagName}` is a variable set by `tags` in swagger.
* `${env}` is a variable set by command option. Default is `dev`.

## Requirement

There is a lot of requirements to use.

### Swagger File

* You need to set `info.title` as service name.
* You need to set `tags` in each path and method to link with Lambda.
* You need to set `securitySchemes` if you use Cognito.
    * default schema name is `ID-Token`.

### AWS

#### System Manager

* You need to set `${serviceName}/${env}/SERVICE_FQDN` as API-Gateway FQDN.
* You need to set `${serviceName}/${env}/COGNITO_USERPOOL_ID`
  as [userpool id in Cognito](https://bobbyhadz.com/blog/aws-cognito-get-identity-pool-id)

#### Lambda

* You need to set name of lambda called by API-Gateway as `${serviceName}${tagName}-${env}`

## Usage

You can use by executing command like `python main.py -i input.yaml -o output.yaml`.

### Options

You can also get helps from command line by executing `python main.py -h`.

* `-i` or `--input` is required for input swagger file path.
* `-o` or `--output` is required for output swagger file path.
* `-e` or `--env` is environment for creating output swagger file. Default is `dev`.
* `--serviceName` is service name for creating output swagger file.
    * default value is `info.title` in swagger file.
* `--awsAccess` is IAM Access Key for pulling value from parameter store.
    * default value is `AWS_ACCESS_KEY_ID` in System environment variable.
* `--awsSecret` is IAM Secret Access Key for pulling value from parameter store.
    * default value is `AWS_SECRET_ACCESS_KEY` in System environment variable.
* `--awsToken` is IAM Acess Session Token for pulling value from parameter store. You need this parameter if you use MFA
  in IAM.
    * default value is `AWS_SESSION_TOKEN` in System environment variable.
* `--format` is format for output swagger file. You can choose `json` or `yaml`.

## Author

[HayatoTakahashi129](https://github.com/HayatoTakahashi129)

## Licence

[MIT](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/LICENCE)