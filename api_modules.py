from typing import Dict
import db
import json
from json_schema import JSONSchema


def check_auth(id: int, token: str) -> bool:
    return db.validate_token(id, token)


class Api:
    def __init__(self):
        self.command_handlers = {}
        self.json_schema = JSONSchema()

    def register_method(self, method: str, handler) -> None:
        print(method, handler)
        self.command_handlers[str(method)] = handler

    def method_calling(self, method_name: str, data: Dict or json):

        if method_name not in self.command_handlers.keys():
            return self.json_schema.generate_error(1)
        user_id = data['id']
        token = data['token']
        if not check_auth(user_id, token):
            return self.json_schema.generate_error(2)
        method = self.command_handlers[method_name]
        resp = method(data)
        if isinstance(resp, str):
            return str(resp)
        return self.json_schema.generate_answer(resp)

    def method(self, method_name: str):
        def wrapper(f):
            self.register_method(method_name, f)
            return f

        return wrapper
