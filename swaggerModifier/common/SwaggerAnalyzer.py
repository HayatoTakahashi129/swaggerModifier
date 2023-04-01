from typing import List, Literal, cast

from swaggerModifier.common.ErrorHandler import show_error

# api methods allowed in open-api
SERVICE_METHODS = ['get', 'post', 'put', 'delete', 'patch']


class SwaggerAnalyzer:
    """
    Analyze Swagger.
    retrieve data from input swagger file.
    """

    def __init__(self, swagger: dict):
        self.swagger: dict = swagger

    def get_all_contained_service_method(self, path: str) -> List[Literal['get', 'post', 'put', 'delete', 'patch']]:
        """
        get all api methods that allowed in open-api.
        :param path: analyze target path
        :return: list of api methods.
        """
        contained_methods: List[Literal['get', 'post', 'put', 'delete', 'patch']] = []
        for method in SERVICE_METHODS:
            if method in self.swagger['paths'][path]:
                contained_methods.append(cast(Literal['get', 'post', 'delete', 'patch'], method))
        if len(contained_methods) == 0:
            show_error(f'There is NO method in {path}.')
        return contained_methods

    def get_all_paths(self) -> List[str]:
        """
        get all path contains in input swagger file.
        :return: list of path in swagger
        """
        if 'paths' not in self.swagger:
            show_error('There is NO `paths` key in input swagger file.')
        return list(dict.keys(self.swagger['paths']))

    def get_tags(self, path: str, method: str) -> List[str]:
        """
        get all tags contains in specific operation in swagger file.
        :param path: api path in swagger
        :param method: api method
        :return: list of tags
        """
        if 'tags' not in self.swagger['paths'][path][method]:
            print('There is NO `tags` key in input swagger file.')
            print(f'path: {path}')
            show_error(f'method: {method}')
        tags: List[str] = list(self.swagger['paths'][path][method]['tags'])
        if len(tags) == 0:
            print('Empty tags was set in input swagger file.')
            print(f'path: ${path}')
            show_error(f'method: {method}')
        return tags

    def has_security(self, path: str, method: str) -> bool:
        """
        check if specific operation in swagger needs security check or not.
        :param path: api method
        :param method: api method
        :return: needs security check or not, boolean.
        """
        if 'security' not in self.swagger['paths'][path][method]:
            return False
        security: list = list(self.swagger['paths'][path][method]['security'])
        return len(security) != 0
