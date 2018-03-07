#_*_coding:utf_8_*_
__author__ = 'dst'
from magweb import MageWeb
from ..model import User,session
from ..util import jsonify
from  .. import config
from webob import exc
import bcrypt
import jwt
import datetime

user_router = MageWeb.Router(prefix='/user')

#token生成
# def gen_token(user_id):
#     return jwt.encode({'user_id':user_id,'timestamp':int(datetime.datetime.now().timestamp())},config.AUTH_SECRET,algorithm='HS256').decode()
def gen_token(user_id):    #口令通过这样获得
    return jwt.encode({
        'user_id':user_id,
        'timestamp':int(datetime.datetime.now().timestamp())
    },config.AUTH_SECRET,algorithm='HS256').decode()

@user_router.post('/reg')
def reg(ctx,request:MageWeb.Request):
    payload = request.json
    print(payload,type(payload))
    email = payload.get('email')
    query = session.query(User).filter(User.email == email).first()
    if query:
        raise exc.HTTPConflict('{} already exists'.format(email))
    user = User()
    try:
        user.name = payload['name']
        user.email = email
        user.password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
    except Exception as e:
        print(e)
        raise exc.HTTPBadRequest()
    session.add(user)
    try:
        session.commit()
        return jsonify(token=gen_token(user.id))
    except Exception as e:
        session.rollback()
        raise exc.HTTPInternalServerError()

@user_router.post('/login')    #需要传入json格式,email,和密码
def login(ctx,request:MageWeb.Request):
    print(request)
    payload = request.json
    print(payload)
    #账号Email验证
    email = payload.get('email')
    #session会话
    #print(session.query())
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise exc.HTTPBadRequest()
    print(user)
    # {
    #     "user": {
    #         "name": "wayne",
    #         "id": 1
    #     },
    #     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aW1lc3RhbXAiOjE1MTc1NTU5MzUsInVzZXJfaWQiOjF9.v_Y-rCzvLQPKJqt9UWYj-kvSGbymRVhQa4TwiSd4X0A"
    # }
    try:
        if bcrypt.checkpw(payload['password'].encode(),user.password.encode()):   #验证密码,密码不正确也不会报错
            print('ok!!!!!!!')    #客户端可以收到返回信息,返回信息包括以上
            return jsonify(user={   #返回为response
                'id':user.id,
                'name':user.name
            },token=gen_token(user.id))
        else:
            print('not ok !')
    except Exception as e:
        print(e)

#@user_router.reg_preinterceptor在路由后执行的拦截器

#对请求过滤,不对登陆login处理 ,验证jwt
def authenticate(handler):   #handler函数的装饰器
    def wrapper(ctx, request: MageWeb.Request):
        print('authen')
        try:
            jwtstr = request.headers.get('Jwt')   #不希望被看到的信息,放在header这中传递
            payload = jwt.decode(jwtstr, config.AUTH_SECRET, algorithms=['HS256'])

            if(datetime.datetime.now().timestamp() - payload.get('timestamp', 0)) > config.AUTH_EXPIRE:
                raise exc.HTTPUnauthorized()
            user_id = payload.get('user_id', -1)
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise exc.HTTPUnauthorized()
            request.user = user
        except Exception as e:
            print(e)
            raise exc.HTTPUnauthorized()
        return handler(ctx, request)
    return wrapper




    # if user and bcrypt.checkpw(payload.get('password').encode(),user.password.encode()):
    #     return jsonify(user={
    #         'id':user.id,
    #         'name':user.name,
    #         'email':user.email
    #     },token = gen_token(user.id))
    # else:
    #     raise exc.HTTPUnauthorized()
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aW1lc3RhbXAiOjE1MTc1NTQzNDMsInVzZXJfaWQiOjF9.htk5o-vQhEVITkXlHGe7igRyPluLBNCWGP7wZ38YHaM