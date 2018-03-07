#_*_coding:utf_8_*_
__author__ = 'dst'
# from blog.handler.test2 import user_router
# from magweb import MageWeb
#
# if __name__ == "__main__":
#     application = MageWeb()
#
#     application.register(user_router)
#
#     from wsgiref import simple_server
#     server = simple_server.make_server('127.0.0.1',9000,application)
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         server.shutdown()
#         server.server_close()

# import json
# jsonstr = """{ "type":"cmdb.types.Int","value":300}"""
# obj = json.loads(jsonstr)
# a= {2:1,4:4}
# print(type(obj))
# print(type(a))

import bcrypt
import datetime
from blog.model import createalltables,Base

from urllib.parse import unquote, quote

url = '姓名'
print(quote(url))
print(unquote(quote(url)))