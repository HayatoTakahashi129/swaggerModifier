# Amplify API-Gateway Swagger Modifier

## Overview

This project purpose is to create swagger file that can import to AWS API-GATEWAY.  
If you try to create swagger file that can import to AWS-API-GATEWAY, you need to add a lot of integrations to swagger
yaml file like `x-amazon-apigateway-integration` but this project will automatically create for you.   
Here is the list that this project will do for you.

* Add [AWS-COGNITO security integrations](https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/api-gateway-swagger-extensions-authorizer.html)
. ([sample](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/sample/output/output.yaml#L362-L367))
* Add [proxy integrations](https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/api-gateway-swagger-extensions-integration.html)
to connect Lambda to each API from tags defined in the
API.([sample](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/sample/output/output.yaml#L57-L61))
* Add `OPTIONS` method to each
API. ([sample](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/sample/output/output.yaml#L252-L288))
  * Add [proxy integrations](https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/api-gateway-swagger-extensions-integration.html)
  in `OPTIONS` method API to
  response [CORS headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#the_http_response_headers) from AWS
  API-GATEWAY. ([sample](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/sample/output/output.yaml#L275-L288))

## Variable Descriptions

There are a few variables in this README.

* `${serviceName}` is a variable set by `info.title` in swagger.
* `${tagName}` is a variable set by `tags` in swagger.
* `${env}` is a variable set by command option. Default is `dev`.

## Requirement

### Swagger File

* You need to set `tags` in each path and method to link with Lambda.
* You need to set `securitySchemes` if you use Cognito.
    * default scheme name is `ID-Token`.

### AWS

#### Lambda

* You need to set name of lambda called by API-Gateway as `${serviceName}${tagName}-${env}`

## Usage

There are 2 ways to use.

- You can use as CLI by executing from python like `python main.py -i input.yaml -o output.yaml`.
- You can use as github workflows.

### Options for CLI

You can also get helps from command line by executing `python main.py -h`.

* `-i` or `--input` is required for input swagger file path.
* `-o` or `--output` is required for output swagger file path.
* `-e` or `--env` is environment for creating output swagger file. Default is `dev`.
* `--serviceName` is service name for creating output swagger file.
    * default value is `info.title` in swagger file.
* `--origin` is required for origin domain used in api.ex:`https://sample-api.com`
* `--cognitoPoolId` is required for cognito authentication. PLEASE set this value from github secrets.
* `--format` is format for output swagger file. You can choose `json` or `yaml`.

### Options for Github Workflows

You can use this project as github action by `HayatoTakahashi129/swaggerModifier@develop`. Here is the list of
parameters in this action.

* `input-file-path`:  required: path of input file in repository
* `output-file-path`: required: path of output file in repository
* `env`:  options: environment for lambda name. default is dev
* `service-name`: options: default is `info.tile` in swagger file
* `origin`:  required: origin for cors header
* `cognito-user-pool-id`: required: cognito user pool id for security
* `output-file-format`: options: output file format. default is yaml

here is the sample for workflow yaml.

```yaml
name: Test Action

on: [ push ]

jobs:
  test-action-is-successful:
    name: execute created action
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: modify sample swagger
        uses: HayatoTakahashi129/swaggerModifier@develop
        with:
          input-file-path: 'sample/sampleTodo.yaml' # required: path of input file in repository
          output-file-path: 'sample/output/output.yaml' # required: path of output file in repository
          env: 'dev' # options: environment for lambda name. default is dev
          service-name: 'sample-todo' # options: default is `info.tile` in swagger file
          origin: 'https://dev.api.sample.com' # required: origin for cors header
          cognito-user-pool-id: 'samplecognitoid2525' # required: cognito user pool id for security 
          output-file-format: 'yaml' # options: output file format. default is yaml
```

## Author

[HayatoTakahashi129](https://github.com/HayatoTakahashi129)

## Licence

[MIT](https://github.com/HayatoTakahashi129/swaggerModifier/blob/develop/LICENCE)