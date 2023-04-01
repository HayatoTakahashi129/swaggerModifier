from typing import List

from swaggerModifier.common.ErrorHandler import show_error

SERVICE_METHODS = ['get', 'post', 'put', 'delete', 'patch']


class SwaggerManager:
    def __init__(self, swagger: dict):
        self.swagger: dict = swagger

    def get_all_contained_service_method(self, path: str) -> List[str]:
        contained_methods: List[str] = []
        for method in SERVICE_METHODS:
            if method in self.swagger['paths'][path]:
                contained_methods.append(method)
        if len(contained_methods) == 0:
            show_error(f'There is NO method in {path}.')
        return contained_methods

    def get_all_paths(self) -> List[str]:
        if 'paths' not in self.swagger:
            show_error('There is NO `paths` key in input swagger file.')
        return list(dict.keys(self.swagger['paths']))

    def get_tags(self, path: str, method: str) -> List[str]:
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
        if 'security' not in self.swagger['paths'][path][method]:
            return False
        security: list = list(self.swagger['paths'][path][method]['security'])
        return len(security) != 0
