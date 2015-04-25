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
    width = Column('width',INTEGER)
    height = Column('height',INTEGER)
    format = Column('format',String)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://catchuser:zfc33786668@127.0.0.1:3306/amusingdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def get_links(rootUrl):
    for page in reversed(range(1,51)):
        links = []
        if rootUrl == 'http://www.hao123.com':
            url = 'http://www.hao123.com/gaoxiao?pn=' + str(page)
            #print 'catchImg: %s' % url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                for item in soup.select('div.gx-item'):
                    content = Item()
                    # content['itemId'] = item.select('a[selector=title]')\
                    #     [0].get('href').split('/')[-1]
                    #标题
                    content.title = item.select('a[selector=title]')[0].get_text().strip()
                    #来源
                    content.source = item.select('span.from a')[0].get_text().strip()
                    #来源链接
                    sourceUrl = item.select('span.from a')[0].get('href').strip()
                    endIdx = sourceUrl.find('?')
                    if endIdx>0:
                        content.source_url = sourceUrl[:endIdx]
                    else:
                        content.source_url = sourceUrl
                    #图片链接
                    content.img_url = item.select('img[selector=pic]')[0].get('img-src').strip()
                    #顶数量
                    content.up_vote = item.select('span[act=up] em.s-nm')[0].get('nm').strip()
                    #踩数量
                    content.down_vote = item.select('span[act=down] em.s-nm')[0].get('nm').strip()
                    #创建时间
                    now = datetime.datetime.now()
                    content.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    links.append(content)
            except requests.exceptions.ConnectionError, e:
                print 'catchImg: %s' % e.message
                return None
            finally:
                pass
        elif rootUrl == 'http://www.juyouqu.com':
            url = 'http://www.juyouqu.com/page/' + str(page)
            #print 'catchImg: %s' % url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                for item in soup.select('div.article'):
                    content = Item()
                    #标题
                    content.title = item.select('div.title a')[0].get_text().strip()
                    #来源
                    content.source = '巨有趣'
                    #来源链接
                    content.source_url = rootUrl + item.select('div.title a')[0].get('href').strip()
                    #图片链接
                    imgUrl = item.select('div.postContainer div.animatedContainerStatic img')[0].get('src')
                    if imgUrl == None:
                        imgUrl = item.select('div.postContainer div.animatedContainerStatic img')[0].get('data-src')
                    content.img_url = imgUrl
                    #顶数量
                    content.up_vote = item.select('div.postContainer div.slideBar span.itemLoveCount')[0].get_text()
                    #踩数量
                    content.down_vote = 0
                    #创建时间
                    now = datetime.datetime.now()
                    content.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    links.append(content)
            except requests.exceptions.ConnectionError, e:
                print 'catchImg: %s' % e.message
                return None
            finally:
                pass
        elif rootUrl == 'http://www.9yaocn.com':
            url = 'http://www.9yaocn.com/neihantu/hot/' + str(page)
            #print 'catchImg: %s' % url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                for item in soup.select('div.conBox'):
                    content = Item()
                    #标题
                    content.title = item.select('h3.boxHeader a')[0].get_text().strip()
                    #来源
                    content.source = '九妖笑话'
                    #来源链接
                    content.source_url = rootUrl + item.select('h3.boxHeader a')[0].get('href').strip()
                    #图片链接
                    imgUrl = item.select('div.videoPlayBox img')[0].get('src')
                    if imgUrl == '/images/loading.gif':
                        imgUrl = item.select('div.videoPlayBox img')[0].get('data-original')
                    content.img_url = imgUrl
                    #顶数量
                    content.up_vote = item.select('div.clearfix a.ding i')[0].get_text()
                    #踩数量
                    content.down_vote = item.select('div.clearfix a.cai i')[0].get_text()
                    #创建时间
                    now = datetime.datetime.now()
                    content.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    links.append(content)
            except requests.exceptions.ConnectionError, e:
                print 'catchImg: %s' % e.message
                return None
            finally:
                pass
        elif rootUrl == 'http://www.budejie.com':
            url = 'http://www.budejie.com/' + str(page)
            #print 'catchImg: %s' % url
            try:
                response = requests.get(url)
                response.encoding='utf-8'
                soup = BeautifulSoup(response.text)
                for item in soup.select('div.web_left'):
                    content = Item()
                    #标题
                    content.title = item.select('div.post-body p.web_size')[0].get_text().strip()
                    print content.title
                    #来源
                    content.source = '百思不得姐'
                    #来源链接
                    content.source_url = item.select('div.post-body a img')[0].get('src').strip()
                    #图片链接
                    # imgUrl =
                    # if imgUrl == '/images/loading.gif':
                    #     imgUrl = item.select('div.videoPlayBox img')[0].get('data-original')
                    content.img_url = item.select('div.post-body a img')[0].get('src')
                    #顶数量
                    content.up_vote = item.select('div.budejie_mutual a.dolove span')[0].get_text()
                    #踩数量
                    content.down_vote = item.select('div.budejie_mutual a.notlove span')[0].get_text()
                    #创建时间
                    now = datetime.datetime.now()
                    content.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    links.append(content)
            except requests.exceptions.ConnectionError, e:
                print 'catchImg: %s' % e.message
                return None
            finally:
                pass
        insert(links)
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
        root_url = ['http://www.hao123.com','http://www.juyouqu.com','http://www.9yaocn.com','http://www.budejie.com']
        print '抓取Img开始'
        pool.map(get_links, root_url)
        print '抓取Img休眠'
        print '开始更新图片宽高格式'
        pool.map(updateImgSize,'0')
        print '更新图片宽高格式休眠'
        time.sleep(3600)

if __name__ == '__main__':
    getImg()
