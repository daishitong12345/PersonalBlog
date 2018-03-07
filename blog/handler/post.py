#_*_coding:utf_8_*_
__author__ = 'dst'
from magweb import MageWeb
from .user import authenticate
from webob import exc
from ..model import Post,Content, session
from ..util import jsonify
import datetime

post_router = MageWeb.Router('/post')

# @post_router.post('/pub')
# @authenticate
# def pub(ctx,request:MageWeb.Request):
#     payload = request.json
#     print(payload)
#     try:
#         title = payload['title']
#         c = payload['content']
#     except:
#         raise exc.HTTPBadRequest()
#     post = Post()
#     post.author_id = request.user.id
#     post.title = title
#     content = Content()
#     content.content = c
#     post.content = content
#
#     session.add(post)
#     print('------------------11')
#     try:
#         print('-----------------2-')
#         session.commit()
#         return jsonify(post_id=post.id)
#     except:
#         session.rollback()
#         raise exc.HTTPInternalServerError()

@post_router.post('/pub')
@authenticate
def pub(ctx,request:MageWeb.Request):
    payload = request.json
    print('post---')
    post = Post()
    try:
        post.title = payload['title']
        post.author_id =request.user.id
        post.postdate = datetime.datetime.now()
        content = Content()
        content.content = payload['content']
        post.content = content
    except:
        raise exc.HTTPBadRequest()
    session.add(post)
    try:
        session.commit()
        print('commited')
        return jsonify(post_id=post.id)
    except:
        session.rollback()
        raise exc.HTTPInternalServerError()
    finally:
        session.close()

@post_router.get('/{id:int}')
def get(ctx,request:MageWeb.Request):
    p_id = request.vars.id
    try:
        post = session.query(Post).filter(Post.id == p_id).one()
        return jsonify(post={
            'post_id':post.id,
            'title':post.title,
            'auther':post.author_id,
            'postdate':post.postdate.timestamp(),
            'content':post.content.content
        })
    except Exception as e:
        print(e)
        raise exc.HTTPNotFound()

