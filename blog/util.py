#_*_coding:utf_8_*_
__author__ = 'dst'
import bcrypt
import json
from magweb import MageWeb

def jsonify(status=200,**kwargs):
    content = json.dumps(kwargs)
    response = MageWeb.Response()
    response.content_type = "application/json"
    response.charset = "UTF-8"
    response.status_code = status
    response.body = "{}".format(content).encode()
    return response


