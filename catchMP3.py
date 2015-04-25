# -*- coding: utf8 -*-
__author__ = 'zhaofucheng'
import sys
import requests
from bs4 import BeautifulSoup
# 导入MySQL驱动:
import mysql.connector
# 导入:
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.databases import *
from sqlalchemy.ext.declarative import declarative_base
# 日期
import datetime
import time
import json
import re

#线程池
from multiprocessing import *

reload(sys)
sys.setdefaultencoding('utf8')

# 创建对象的基类:
Base = declarative_base()

# 定义声音专辑对象:
class SoundAlbum(Base):
    # 表的名字
    __tablename__ = 'a_amusing_album'

    # 表的结构:
    album_id = Column('album_id',String, primary_key=True)
    album_title = Column('album_title',String)
    album_source = Column('album_source',String)
    album_url = Column('album_url',String)
    album_img = Column('album_img',String)
    album_play_count = Column('album_play_count',INTEGER)
    tag_list = Column('tag_list',String)
    sound_count = Column('sound_count',INTEGER)
    create_time = Column('create_time',String)
    update_time = Column('update_time',String)
# 定义声音对象
class Sound(Base):
    # 表的名字
    __tablename__ = 'a_amusing_audio'

    # 表的结构
    id = Column('id',String,primary_key=True)
    album_id = Column('album_id',String)
    album_title = Column('album_title',String)
    category_name = Column('category_name',String)
    category_title = Column('category_title',String)
    comments_count = Column('comments_count',INTEGER)
    cover_url = Column('cover_url',String)
    cover_url_142 = Column('cover_url_142',String)
    duration = Column('duration',FLOAT)
    favorites_count = Column('favorites_count',INTEGER)
    formatted_created_at = Column('formatted_created_at',String)
    have_more_intro = Column('have_more_intro',String)
    intro = Column('intro',String)
    is_favorited = Column('is_favorited',String)
    nickname = Column('nickname',String)
    play_count = Column('play_count',INTEGER)
    play_path = Column('play_path',String)
    play_path_32 = Column('play_path_32',String)
    play_path_64 = Column('play_path_64',String)
    play_path_128 = Column('play_path_128',String)
    played_secs = Column('played_secs',String)
    shares_count = Column('shares_count',INTEGER)
    short_intro = Column('short_intro',String)
    time_until_now = Column('time_until_now',String)
    title = Column('title',String)
    uid = Column('uid',String)
    create_time = Column('create_time',String)
    update_time = Column('update_time',String)
    in_albums = Column('in_albums',String)

    def __init__(self, id, album_id, album_title, category_name, category_title, comments_count,
                 cover_url, cover_url_142, duration, favorites_count, formatted_created_at, have_more_intro,
                 intro, is_favorited, nickname, play_count, play_path, play_path_32, play_path_64, play_path_128,
                 played_secs, shares_count, short_intro, time_until_now, title, uid):
        self.id = id
        self.album_id = album_id
        self.album_title = album_title
        self.category_name = category_name
        self.category_title = category_title
        self.comments_count = comments_count
        self.cover_url = cover_url
        self.cover_url_142 = cover_url_142
        self.duration = duration
        self.favorites_count = favorites_count
        self.formatted_created_at = formatted_created_at
        self.have_more_intro = have_more_intro
        self.intro = intro
        self.is_favorited = is_favorited
        self.nickname = nickname
        self.play_count = play_count
        self.play_path = 'http://fdfs.xmcdn.com/' + play_path
        if play_path_32 != None:
            self.play_path_32 = 'http://fdfs.xmcdn.com/' + play_path_32
        else:
            self.play_path_32 = play_path_32

        if play_path_64 != None:
            self.play_path_64 = 'http://fdfs.xmcdn.com/' + play_path_64
        else:
            self.play_path_64 = play_path_64

        if play_path_128 != None:
            self.play_path_128 = 'http://fdfs.xmcdn.com/' + play_path_128
        else:
            self.play_path_128 = play_path_128

        self.played_secs = played_secs
        self.shares_count = shares_count
        self.short_intro = short_intro
        self.time_until_now = time_until_now
        self.title = title
        self.uid = uid

    def sound2dict(sound):
        return {
            'id' : sound.id,
            'album_id' : sound.album_id,
            'album_title' : sound.album_title,
            'category_name' : sound.category_name,
            'category_title' : sound.category_title,
            'comments_count' : sound.comments_count,
            'cover_url' : sound.cover_url,
            'cover_url_142' : sound.cover_url_142,
            'duration' : sound.duration,
            'favorites_count' : sound.favorites_count,
            'formatted_created_at' : sound.formatted_created_at,
            'have_more_intro' : sound.have_more_intro,
            'intro' : sound.intro,
            'is_favorited' : sound.is_favorited,
            'nickname' : sound.nickname,
            'play_count' : sound.play_count,
            'play_path' : sound.play_path,
            'play_path_32' : sound.play_path_32,
            'play_path_64' : sound.play_path_64,
            'play_path_128' : sound.play_path_128,
            'played_secs' : sound.played_secs,
            'shares_count' : sound.shares_count,
            'short_intro' : sound.short_intro,
            'time_until_now' : sound.time_until_now,
            'title' : sound.title,
            'uid' : sound.uid
        }

def dict2sound(d):
    return Sound(d['id'], d['album_id'], d['album_title'], d['category_name'],
                 d['category_title'], d['comments_count'],d['cover_url'], d['cover_url_142'],
                 d['duration'], d['favorites_count'], d['formatted_created_at'], d['have_more_intro'],
                 d['intro'], d['is_favorited'], d['nickname'], d['play_count'], d['play_path'],
                 d['play_path_32'], d['play_path_64'], d['play_path_128'], d['played_secs'],
                 d['shares_count'], d['short_intro'], d['time_until_now'], d['title'], d['uid'])

# 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://user01:123456@127.0.0.1:3306/testdb')
engine = create_engine('mysql+mysqlconnector://catchuser:zfc33786668@127.0.0.1:3306/amusingdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def get_album_links(page):
    links = []
    url = 'http://album.ximalaya.com/dq/entertainment/' + str(page)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        for item in soup.select('div.discoverAlbum_item'):
            album = SoundAlbum()
            album.album_id = item.get('album_id').strip()
            album.album_url = item.select('div.albumfaceOutter a')[0].get('href').strip()
            album.album_img = item.select('div.albumfaceOutter a img')[0].get('src').strip()
            album.album_play_count = item.select('div.albumfaceOutter span.sound_playcount')[0].get_text().strip()
            album.album_title = item.select('a.discoverAlbum_title')[0].get('title').strip()
            album.album_source = '喜马拉雅'
            #创建时间
            now = datetime.datetime.now()
            album.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
            album.update_time = now.strftime('%Y-%m-%d %H:%M:%S')
            links.append(album)
    except requests.exceptions.ConnectionError,e:
        print e.message
        return None
    finally:
        pass

    album_insert_or_update(links)


def get_sound_links(url,page,pageCount):
    albumId = url[url.rfind('/')+1:]
    try:
        pageStr = ''
        if page > 1:
            pageStr = '?page='+str(page)
        response = requests.get(url+pageStr)
        soup = BeautifulSoup(response.text)
        pageList = soup.select('a.pagingBar_page')
        if len(pageList) > 0 and pageCount==0:
            pageCount = pageList[-2].get_text()
            # <a class="pagingBar_page" hashlink="" href="/11961469/album/269483?page=2">2</a>
        for sound in soup.select('div.album_soundlist li'):
            # print sound.select('a.title')[0].get('title')
            # fwd = sound.select('span.fwd')
            # if fwd !=None and len(fwd) > 0:
            #     print fwd[0].get_text().strip()
            get_sound(sound.get('sound_id'),albumId)
            # pass

        if int(page) == 1:
            album = SoundAlbum()
            album.album_id = url[url.rfind('/')+1:]
            tag_list = ''
            for span in soup.select('div.tagBtnList a.tagBtn2'):
                tag_list += span.select('span')[0].get_text() + ' '
            album.tag_list = tag_list
            sound_count = soup.select('span.albumSoundcount')[0].get_text()

            pattern = re.compile(r'\d*')
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            album.sound_count = pattern.findall(sound_count)[1]

            #创建时间
            now = datetime.datetime.now()
            album.update_time = now.strftime('%Y-%m-%d %H:%M:%S')

            album_update_tagList_soundCount(album)


        if int(page)>=int(pageCount):
            return
        else:
            get_sound_links(url,page+1,pageCount)
    except requests.exceptions.ConnectionError,e:
        print 'catchMp3:%s' % e.message

def get_sound(soundId,albumId):
    # http://www.ximalaya.com/tracks/4718853.json
    root_url = 'http://www.ximalaya.com/tracks/'
    try:
        response = requests.get(root_url+soundId+'.json')
        # print response.text
        sound = json.loads(response.text, object_hook=dict2sound)
        sound_insert_or_update(sound,albumId)
    except Exception,e:
        print e.message
    finally:
        pass


def sound_insert_or_update(sound,albumId):
    session = DBSession()
    try:
        isExists = session.query(exists().where(Sound.id==sound.id)).scalar()
        if isExists:
            # print 'catchMp3:Update : %s' % sound.id
            oldSound = session.query(Sound).filter(Sound.id==sound.id).one()
            inAlbums = oldSound.in_albums
            if oldSound.in_albums.find(albumId)==-1:
                inAlbums = oldSound.in_albums + ','+ albumId
            now = datetime.datetime.now()
            sound.update_time = now.strftime('%Y-%m-%d %H:%M:%S')
            stmt = update(Sound).where(Sound.id==sound.id).values(cover_url=sound.cover_url,
                                                                    cover_url_142=sound.cover_url_142,
                                                                    comments_count=sound.comments_count,
                                                                    favorites_count = sound.favorites_count,
                                                                    play_count = sound.play_count,
                                                                    shares_count = sound.shares_count,
                                                                    time_until_now = sound.time_until_now,
                                                                    update_time=sound.update_time,
                                                                    in_albums=inAlbums)
            session.execute(stmt)
        else:
            # print 'catchMp3:Insert : %s' % sound.id
            #创建时间
            now = datetime.datetime.now()
            sound.create_time = now.strftime('%Y-%m-%d %H:%M:%S')
            sound.update_time = now.strftime('%Y-%m-%d %H:%M:%S')
            sound.in_albums = albumId
            session.add(sound)
    except Exception,e:
        print e.message
    finally:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()


def album_insert_or_update(albums):
    if albums == None:
        return
    session = DBSession()
    try:
        for album in albums:
            isExists = session.query(exists().where(SoundAlbum.album_id==album.album_id)).scalar()
            if isExists:
               # print 'catchMp3:Update : %s' % album
                now = datetime.datetime.now()
                album.update_time = now.strftime('%Y-%m-%d %H:%M:%S')
                stmt = update(SoundAlbum).where(SoundAlbum.album_id==album.album_id).values(album_play_count=album.album_play_count,album_img = album.album_img,
                                                                                            album_title = album.album_title,
                                                                                            update_time=album.update_time)
                session.execute(stmt)
            else:
               # print 'catchMp3:Insert : %s' % album
                session.add(album)
    except Exception,e:
        print e.message
    finally:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

def album_update_tagList_soundCount(album):
    session = DBSession()
    try:
        #print 'catchMp3:Update : %s' % album
        stmt = update(SoundAlbum).where(SoundAlbum.album_id==album.album_id).values(tag_list=album.tag_list,
                                                                                    sound_count=album.sound_count,
                                                                                    update_time=album.update_time)
        session.execute(stmt)
    except Exception,e:
        print e.message
    finally:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

#def get_sound_album_links_from_mysql():
#    list = []
#    # 创建Session:
#    session = DBSession()
#    try:
#        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
#        list = session.query(SoundAlbum).all()
#    except Exception,e:
#        print e.message
#        return None
#    finally:
#        # 关闭Session:
#        session.close()
#    return list

def get_sound_album_links_from_mysql(page):
    list = []
    # 创建Session:
    session = DBSession()
    try:
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        list = session.query(SoundAlbum).slice(0+int(page)*50,50+int(page)*50).all()
        if len(list) > 0:
            # print list
            for album in list:
                # print album.album_url
                get_sound_links(album.album_url,1,0)
            session.close()
            get_sound_album_links_from_mysql(int(page)+1)
        else:
            return None
    except Exception,e:
        print e.message
        return None
    finally:
        # 关闭Session:
        session.close()
    return None

def getMp3():
    pool = Pool(processes=2)
    while True:
        print '抓取Mp3开始'
        pool.map(get_album_links, reversed(range(1,31)))
        pool.map(get_sound_album_links_from_mysql,'0')
        print '抓取Mp3休眠'
        time.sleep(3600*6)

        # get_sound_links('http://www.ximalaya.com/2629577/album/203355',1,0)

if __name__ == '__main__':
    getMp3()
