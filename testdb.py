# -*- coding: utf8 -*-
# 导入MySql驱动:
import mysql.connector
import os
import json
import sys

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.databases import *
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.restful import Resource, fields, marshal_with, marshal

reload(sys)
sys.setdefaultencoding('utf8')

# 创建对象的基类:
Base = declarative_base()

# 定义搞笑图片对象:
class Img(Base):
    # 表的名字:
    __tablename__ = 'a_amusing_img'

    # 表的结构:
    item_id = Column('item_id',INTEGER, primary_key=True)
    title = Column('title',String)
    source = Column('source',String)
    source_url = Column('source_url',String)
    img_url = Column('img_url',String)
    up_vote = Column('up_vote',INTEGER)
    down_vote = Column('down_vote',INTEGER)
    create_time = Column('create_time',String)

img_fields = {
    'item_id':Img.item_id,
    'title':Img.title,
    'source':Img.title,
    'source_url':Img.source_url,
    'up_vote':Img.up_vote,
    'down_vote':Img.down_vote,
    'create_time':Img.create_time
}

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://catchuser:zfc33786668@127.0.0.1:3306/amusingdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    img = session.query(Img).filter(Img.item_id=='9550').one()
    session.close()
    #print img
    print json.dumps(marshal(img, img_fields))
