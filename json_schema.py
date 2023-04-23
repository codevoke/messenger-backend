from typing import Dict


class JSONSchema:
    errors = {
        0: "Произошла неизвестная ошибка.",
        1: "Передан неизвестный метод.",
        2: "Авторизация пользователя не удалась.",
        3: "Слишком много запросов в секунду.",
        4: "Нет прав для выполнения этого действия.",
        5: "Произошла внутренняя ошибка сервера.",
        6: "Доступ запрещён."
    }

    def generate_error(self,
                       error_code: int,
                       request_params: Dict[str, str] = None,
                       error_description_message: str = None) -> Dict:
        json_request_params = []
        if request_params:
            for param in request_params.keys():
                json_request_params.append({
                    "key": param,
                    "value": request_params[param]
                })

        error = {
            "error":
                {
                    "error_code": error_code,
                    "error_msg": f"{self.errors[error_code]} : {error_description_message}",
                },
            "request_params": json_request_params
        }

        return error

    def generate_answer(self,
                        response: Dict):
        answer = {
            "response": dict(response)
        }
        return answer
