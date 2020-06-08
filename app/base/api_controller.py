import traceback

from flask import jsonify

from .controller import Controller


class APIErrorException(Exception):
    code = -1
    msg = '服务器错误，请联系管理员进行处理。'


class APIController(Controller):
    class ParamsNotMatchException(APIErrorException):
        code = -2
        msg = 'API调用参数错误。'

    def _response_func(self, view_func, *args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except APIErrorException as e:
            return jsonify(error=e.code, msg=e.msg, exc=traceback.format_exc())
        except:
            return jsonify(error=APIErrorException.code, exc=traceback.format_exc())

    def make_response(self, error=0, **data):
        return jsonify(dict(error=error, data=data))
