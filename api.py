from api_modules import Api

ServerApi = Api()


@ServerApi.method(method_name='accept')
def accept(data):
    return {"accept": True}
