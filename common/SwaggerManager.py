from typing import List

import config

service_methods = ['get', 'post']


class SwaggerManager:
    def __init__(self, swagger: dict):
        self.swagger: dict = swagger

    def get_all_contained_service_method(self, path: str) -> List[str]:
        contained_methods: List[str] = []
        for method in service_methods:
            if method in self.swagger['paths'][path]:
                contained_methods.append(method)
        return contained_methods

    def get_all_paths(self) -> List[str]:
        return list(dict.keys(self.swagger['paths']))

    def get_tags(self, path: str, method: str) -> List[str]:
        return list(self.swagger['paths'][path][method]['tags'])

    def get_service_name(self) -> str:
        if config.SERVICE_NAME is not None:
            return config.SERVICE_NAME
        return self.swagger['info']['title']

    def has_security(self, path: str, method: str) -> bool:
        security: list = list(self.swagger['paths'][path][method]['security'])
        return len(security) != 0
