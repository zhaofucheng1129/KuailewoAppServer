# -*- coding: utf8 -*-
__author__ = 'zhaofucheng'
import requests
from bs4 import BeautifulSoup
import sys
# 导入MySQL驱动:
import mysql.connector
# 日期
import datetime
import time
import re

# 导入:
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.databases import *
from sqlalchemy.ext.declarative import declarative_base

#线程池
from multiprocessing import *

import cStringIO, urllib2, Image

reload(sys)
sys.setdefaultencoding('utf8')
# 设置递归深度
sys.setrecursionlimit(1000000) #例如这里设置为一百万 默认900

# 创建对象的基类:
Base = declarative_base()

# 定义搞笑图片对象:
class Item(Base):
    # 表的名字:
    __tablename__ = 'a_amusing_beauty'

    # 表的结构:
    item_id = Column('item_id',INTEGER, primary_key=True)
    title = Column('title',String)
    source = Column('source',String)
    source_url = Column('source_url',String)
    img_url = Column('img_url',String)
    up_vote = Column('up_vote',INTEGER)
    down_vote = Column('down_vote',INTEGER)
    create_time = Column('create_time',String)
    width = Column('width',INTEGER)
    height = Column('height',INTEGER)
    format = Column('format',String)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://catchuser:zfc33786668@127.0.0.1:3306/amusingdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def get_links(rootUrl):
    links = []
    if rootUrl == 'http://www.mm131.com/xinggan/':
        url = 'http://www.mm131.com/xinggan/list_6_1.html'
        response = requests.get(url)
        response.encoding='gbk'
        soup = BeautifulSoup(response.text)
        page = soup.select('div.main dd.page a.page-en')[-1].get('href').strip()
        pattern = re.compile(r'\d*')
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        page = pattern.findall(page)[7]
        for page in reversed(range(1,int(page)+1)):
            pageUrl = 'http://www.mm131.com/xinggan/list_6_'+str(page)+'.html'
            try:
                response = requests.get(pageUrl)
                response.encoding='gbk'
                soup = BeautifulSoup(response.text)
                for item in soup.select('dl.list-left a[target=_blank]'):
                    link = item.get('href').strip()
                    rs = requests.get(link)
                    rs.encoding='gbk'
                    s = BeautifulSoup(rs.text)
                    pageCount = s.select('span.page-ch')[0].get_text().strip()

                    pattern = re.compile(r'\d*')
                    pageCount = pattern.findall(pageCount)[1]

                    pageId = s.select('a.page-ch')[0].get('href').strip()
                    pattern = re.compile(r'\d*')
                    pageId = pattern.findall(pageId)[0]
                    # print pageId

                    contentArr = []
                    for p in range(1,int(pageCount)+1):
                        # http://www.mm131.com/xinggan/511.html
                        albumUrl = ''
                        if p == 1:
                            albumUrl = link
                        else:
                            albumUrl = 'http://www.mm131.com/xinggan/' + pageId + '_' + str(p) + '.html'
                        c = requests.get(albumUrl)
                        c.encoding='gbk'
                        csoup = BeautifulSoup(c.text)

                        content = Item()
                        # 标题
                        content.title = csoup.select('div.content h5')[0].get_text().strip()
                        #来源
                        content.source = 'mm131'
                        #来源链接
                        content.source_url = csoup.select('div.content-pic img')[0].get('src').strip()

                        #图片链接
                        content.img_url = csoup.select('div.content-pic img')[0].get('src').strip()
                        #顶数量
                        content.up_vote = 0
                        #踩数量
                        content.down_vote = 0
                        #创建时间
                        now = datetime.datetime.now()
                        content.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
                        contentArr.append(content)
                    insert(contentArr)
            except requests.exceptions.ConnectionError, e:
                print 'catchImg: %s' % e.message
                return None
            finally:
                pass

    return None

def insert(contents):
    if contents == None:
        return
    session = DBSession()
    try:
        for content in contents:
            isExists = session.query(exists().where(Item.source_url==content.source_url)).scalar()
            if not isExists:
                # 创建session对象:
                # 添加到session:
               # print 'catchImg: Insert : %s' % content
                session.add(content)

    except Exception,e:
        print e.message
    finally:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

def updateImgSize(page):
    session = DBSession()
    try:
        countNum = session.query(func.count(Item.item_id)).order_by(Item.create_time.desc()).filter(Item.width==None).one()[0]
        # print countNum
        if countNum>0:
            sourceImgs = session.query(Item).order_by(Item.create_time.desc()).filter(Item.width==None).slice(0,50).all()
            for img in sourceImgs:
                file = urllib2.urlopen(img.img_url)
                tmpIm = cStringIO.StringIO(file.read())
                im = Image.open(tmpIm)
                # print im.format, im.size[0],im.size[1], im.mode
                stmt = update(Item).where(Item.item_id==img.item_id).values(width=im.size[0],
                                                                      height = im.size[1],
                                                                      format = im.format)
                session.execute(stmt)
            # 提交即保存到数据库:
            session.commit()
            # 关闭session:
            session.close()

            # print int(page)+1
            updateImgSize(int(page)+1)
        else:
            return
    except Exception,e:
        print e.message
    finally:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

def getImg():
    pool = Pool(processes=2)
    while True:
        root_url = ['http://www.mm131.com/xinggan/']
        print '抓取Img开始'
        pool.map(get_links, root_url)
        print '抓取Img休眠'
        print '开始更新图片宽高格式'
        pool.map(updateImgSize,'0')
        print '更新图片宽高格式休眠'
        time.sleep(3600)

if __name__ == '__main__':
    getImg()