from typing import Dict
import db
import json
from json_schema import JSONSchema


def check_auth(id: int, token: str) -> bool:
    return db.validate_token(id, token)


class Api:
    def __init__(self):
        self.command_handlers = None
        self.json_schema = JSONSchema()

    def register_method(self, method: str, handler) -> None:
        self.method_handlers[method] = handler

    def method_calling(self, method_name: str, data: Dict or json):
        if method_name not in self.method_handlers.keys():
            self.json_schema.generate_error(1)
        id = data['id']
        token = data['token']
        if not check_auth(id, token):
            return self.json_schema.generate_error(2)
        method_handler = self.method_handlers.get(method_name)
        try:
            response = method_handler(data)
            return self.json_schema.generate_answer(response)
        except BaseException:
            return self.json_schema.generate_error(0)


    def method(self, method_name: str):
        def wrapper(f):
            self.register_method(method_name, f)
            return f

        return wrapper
