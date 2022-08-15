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

* You need to set `${serviceName}/${env}/serviceFQDN` as API-Gateway FQDN.
* You need to set `${serviceName}/${env}/Cognito-userpool-id`
  as [userpool id in Cognito](https://bobbyhadz.com/blog/aws-cognito-get-identity-pool-id)

#### Lambda

* You need to set name of lambda called by API-Gateway as `${serviceName}/${tagName}-${env}`

## Usage

You can use by executing command like `python main.py -i input.yaml -o output.yaml`.

### Options

You can also get helps from command line by executing `python main.py -h`.

* `-i` or `--input` is required for input swagger file path.
* `-o` or `--output` is required for output swagger file path.
* `-e` or `--env` is environment for creating output swagger file. Default is `dev`.

## Author

[HayatoTakahashi129](https://github.com/HayatoTakahashi129)

## Licence

[MIT](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/LICENCE)