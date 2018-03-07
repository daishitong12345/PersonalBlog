#_*_coding:utf_8_*_
__author__ = 'dst'

from webob.dec import wsgify
from webob import Response,Request ,exc
import re

class DictObj:  #属性访问并且不能赋值
    def __init__(self,d:dict):
        if not isinstance(d,dict):
            self.__dict__['_dict'] = {}
        else:
            self.__dict__['_dict'] = d
    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format(item))
    def __setattr__(self, key, value):
        raise NotImplementedError

class Context(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format((item)))
    def __setattr__(self, key, value):
        self[key] = value

class NestedContext(Context):
    def __init__(self,globalcontext:Context=None):
        super().__init__()
        self.relate(globalcontext)
    def relate(self,globalcontext:Context=None):
        self.globalcontext = globalcontext

    def __getattr__(self, item):
        if item in self.keys():
            return self[item]
        return self.globalcontext[item]

class _Router:
    TYPEPATTERNS = {
        'str': r'[^/]+',
        'word': r'\w+',
        'int': r'[+-]?\d+',
        'float': r'[+-]?\d+\.\d+',
        'any': r'.+'
    }
    TYPECAST = {
        'str': str,
        'word': str,
        'int': int,
        'float': float,
        'any': str
    }
    KVPATTERN = re.compile(r'/({[^{}:]+:?[^{}:]*})')

    def _transfrom(self,kv: str):
        name, _, type = kv.strip('/{}').partition(':')
        return '/(?P<{}>{})'.format(name, self.TYPEPATTERNS.get(type, '\w+')), name, self.TYPECAST.get(type, str)

    def _parse(self,src: str):
        start = 0
        res = ''
        translator = {}  # id => int
        while True:
            matcher = self.KVPATTERN.search(src, start)
            if matcher:
                res += matcher.string[start:matcher.start()]  # matcher.start()返回组的序号
                tmp = self._transfrom(matcher.string[matcher.start():matcher.end()])
                res += tmp[0]
                translator[tmp[1]] = tmp[2]
                start = matcher.end()
            else:
                break
        if res:
            return res, translator
        else:
            return src, translator

    def __init__(self,prefix:str=""):
        self.__prefix = prefix.rstrip('/\\')
        self.__routetable = []
        #拦截器
        self.pre_interceptor = []
        self.post_interceptor = []
        #上下文
        self.ctx = NestedContext()

    @property
    def prefix(self):
        return self.__prefix

    def register_preinterceptor(self,fn):
        self.pre_interceptor.append(fn)
        return fn

    def route(self, rule,*methods):
        def wrapper(handler):
            #把对象化的正则表达式存入
            pattern,translator = self._parse(rule)
            self.__routetable.append((re.compile(pattern),handler,translator,methods))
            return handler   #如果使用了多层装饰器需要返回handler
        return wrapper

    def get(self,pattern):
        return self.route(pattern,"GET")

    def post(self,pattern):
        return self.route(pattern,"POST")

    def match(self,request:Request) -> Response:
        if not request.path.startswith(self.__prefix):
            return None
        for pattern,handler,translator,methods in self.__routetable:
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.__prefix,'',1))
                if matcher:
                    newdict = {}
                    for k,v in matcher.groupdict().items():
                        newdict[k] = translator[k](v)
                    request.vars = DictObj(newdict)
                    #return handler(request)
                    response = handler(self.ctx,request)
                    for fn in self.post_interceptor:
                        response = fn(self.ctx,request,response)
                    return response
class MageWeb:
    Router = _Router
    Request = Request
    Response = Response

    ctx = Context()
    def __init__(self,**kwargs):
        self.ctx.app = self
        for k,v in kwargs:
            self.ctx[k] = v
    ROUTERS = []
    #拦截器
    PRE_INTERCEPTOR = []
    POST_INTERCEPTOR = []

    @classmethod
    def register_preinterceptor(cls,fn):
        cls.PRE_INTERCEPTOR.append(fn)
        return fn
    @classmethod
    def register_postinterceptor(cls,fn):
        cls.POST_INTERCEPTOR.append(fn)
        return fn
    @classmethod
    def register(cls,router:_Router):
        router.ctx.relate(cls.ctx)
        router.ctx.router = router
        cls.ROUTERS.append(router)

    @wsgify
    def __call__(self, request:Request) ->Response:
        for fn in self.PRE_INTERCEPTOR:     #匹配路由前拦截
            request = fn(self.ctx,request)
        for router in self.ROUTERS:
            response = router.match(request)
            for fn in self.POST_INTERCEPTOR:   #匹配路由后拦截
                response = fn(self.ctx,request,response)
            if response:
                return response
        raise exc.HTTPNotFound('你访问的页面被外星人劫持了')

    @classmethod
    def extend(cls,name,ext):
        cls.ctx[name] = ext

