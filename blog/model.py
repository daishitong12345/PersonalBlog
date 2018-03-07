#_*_coding:utf_8_*_
__author__ = 'dst'
from sqlalchemy import Column,Integer,BigInteger,String,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT
from .import config

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(48),nullable=False)
    email = Column(String(64),nullable=False,unique=True)
    password = Column(String(128),nullable=False)

    def __repr__(self):
        return "<User (id={},name={},email={})>".format(self.id,self.name,self.email)

class Post(Base):
    __tablename__= "post"
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    title = Column(String(250),nullable=False)
    author_id = Column(Integer,ForeignKey('user.id'),nullable=False)
    postdate = Column(DateTime,nullable=False)

    author = relationship('User')
    content = relationship('Content',uselist=False)

    def __repr__(self):
        return "<Post (id={},title={})>".format(self.id,self.title)


class Content(Base):
    __tablename__ = "content"
    id = Column(BigInteger,ForeignKey('post.id'),primary_key=True)
    content = Column(LONGTEXT,nullable=False)
    def __repr__(self):
        return "<Content (id={},content={})>".format(self.id,self.content[:20])


# class Test(Base):
#     __tablename__ = "modeltest"
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     date = Column(DateTime,nullable=True)
engine = create_engine(config.URL,echo=config.DATABASE_DEBUG)

def createalltables():
    Base.metadata.create_all(engine)
def droptallbles():
    Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)

session = Session()   #建立数据库session 绑定ip

