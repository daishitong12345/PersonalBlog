#_*_coding:utf_8_*_
__author__ = 'dst'
from magweb import MageWeb
from ..model import User,session
from ..util import jsonify

user_router = MageWeb.Router(prefix='/user')

@user_router.post('/reg')
def reg(ctx,request:MageWeb.Request):
    print(request)

@user_router.post('/login')
def login(ctx,request:MageWeb.Request):
    print(request)
