#_*_coding:utf_8_*_
__author__ = 'dst'

from magweb import MageWeb
from blog import config
from blog.handler.user import user_router
from blog.handler.post import post_router

if __name__ == "__main__":
    application = MageWeb()
    application.register(user_router)
    application.register(post_router)
    from wsgiref import simple_server
    server = simple_server.make_server(config.WSIP,config.WSPORT,application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()