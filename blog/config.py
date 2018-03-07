#_*_coding:utf_8_*_
__author__ = 'dst'
USERNAME = 'root'
PASSWD = '123456'
IP = '192.168.150.129'
PORT = 3306
DBNAME ='blog'
PARAMS = "charset=utf8"
# url ='mysql+pymysql://dst:123456@172.16.101.8:3306/blog?charset=utf8'
URL = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USERNAME,PASSWD,IP,PORT,DBNAME,PARAMS)
DATABASE_DEBUG = True
WSIP = '127.0.0.1'
WSPORT = 9000
AUTH_SECRET = "www.magedu.com"   #和网站无关
AUTH_EXPIRE = 8*60*60