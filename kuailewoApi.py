# -*- coding: utf8 -*-
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

import json

# 导入MySql驱动:
import mysql.connector

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.databases import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import cast

#创建对象的基类:
Base = declarative_base()

#定义搞笑图片对象:
class Img(Base):
    #表的名字:
    __tablename__ = 'a_amusing_img'

    #表的结构:
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

    def dict(img):
        return{
            'item_id':img.item_id,
            'title':img.title,
            'source':img.source,
            'source_url':img.source_url,
            'img_url':img.img_url,
            'up_vote':img.up_vote,
            'down_vote':img.down_vote,
            'create_time':img.create_time,
            'width':img.width,
            'height':img.height,
            'format':img.format
        }

#定义美女图片对象:
class BeautyGirlImg(Base):
    #表的名字:
    __tablename__ = 'a_amusing_beauty'

    #表的结构:
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

    def dict(img):
        return{
            'item_id':img.item_id,
            'title':img.title,
            'source':img.source,
            'source_url':img.source_url,
            'img_url':img.img_url,
            'up_vote':img.up_vote,
            'down_vote':img.down_vote,
            'create_time':img.create_time,
            'width':img.width,
            'height':img.height,
            'format':img.format
        }
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

    def soundAlbum2dict(soundAlbum):
        return{
            'album_id':soundAlbum.album_id,
            'album_title':soundAlbum.album_title,
            'album_source':soundAlbum.album_source,
            'album_url':soundAlbum.album_url,
            'album_img':soundAlbum.album_img,
            'album_play_count':soundAlbum.album_play_count,
            'tag_list':soundAlbum.tag_list,
            'sound_count':soundAlbum.sound_count,
            'create_time':soundAlbum.create_time,
            'update_time':soundAlbum.update_time
        }
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
            'uid' : sound.uid,
            'create_time' : sound.create_time,
            'update_time' : sound.update_time
        }



# engine = create_engine('mysql+mysqlconnector://user01:123456@127.0.0.1:3306/testdb')
engine = create_engine('mysql+mysqlconnector://catchuser:zfc33786668@127.0.0.1:3306/amusingdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/api/img', methods=['GET'])
def api_get_img():
    since_id = request.args.get('since_id')
    before_id = request.args.get('before_id')
    count = request.args.get('count')
    if since_id == None:
        since_id = 0
    if before_id == None:
        before_id = 0
    if count == None:
        count = 20

    #创建Session:
    session = DBSession()
    try:
        imgs = []
        if since_id != 0:
            imgs = session.query(Img).filter(Img.item_id>since_id).filter(Img.width!=None).order_by(Img.item_id.desc()).slice(0,int(count)).all()
        elif before_id != 0:
            imgs = session.query(Img).filter(Img.item_id<before_id).filter(Img.width!=None).order_by(Img.item_id.desc()).slice(0,int(count)).all()
        else:
            imgs = session.query(Img).filter(Img.width!=None).order_by(Img.item_id.desc()).slice(0,int(count)).all()
        session.close()


        jsonArr = []
        for img in imgs:
            jsonArr.append(img.dict())
        jsonValue = json.dumps(jsonArr)
        resp = Response(jsonValue, status=200, mimetype='application/json')
        return resp
    except Exception,e:
        print e.message
    finally:
        # 关闭session:
        session.close()

@app.route('/api/beautyImg', methods=['GET'])
def api_get_beautyImg():
    since_id = request.args.get('since_id')
    before_id = request.args.get('before_id')
    count = request.args.get('count')
    if since_id == None:
        since_id = 0
    if before_id == None:
        before_id = 0
    if count == None:
        count = 20

    #创建Session:
    session = DBSession()
    try:
        imgs = []
        if since_id != 0:
            imgs = session.query(BeautyGirlImg).filter(BeautyGirlImg.item_id>since_id).filter(BeautyGirlImg.width!=None).order_by(BeautyGirlImg.item_id).slice(0,int(count)).all()
        elif before_id != 0:
            imgs = session.query(BeautyGirlImg).filter(BeautyGirlImg.item_id<before_id).filter(BeautyGirlImg.width!=None).order_by(BeautyGirlImg.item_id).slice(0,int(count)).all()
        else:
            imgs = session.query(BeautyGirlImg).filter(BeautyGirlImg.width!=None).order_by(BeautyGirlImg.item_id).slice(0,int(count)).all()
        session.close()


        jsonArr = []
        for img in imgs:
            jsonArr.append(img.dict())
        jsonValue = json.dumps(jsonArr)
        resp = Response(jsonValue, status=200, mimetype='application/json')
        return resp
    except Exception,e:
        print e.message
    finally:
        # 关闭session:
        session.close()

@app.route('/api/soundAlbum', methods=['GET'])
def api_get_soundAlbums():
    page = request.args.get('page')
    if page == None:
        page = 0
    #创建Session:
    session = DBSession()
    try:
        soundAlbums = session.query(SoundAlbum).order_by(SoundAlbum.album_play_count.desc()).slice(0+int(page)*20,20+int(page)*20).all()
        session.close()

        jsonArr = []
        for soundAlbum in soundAlbums:
            jsonArr.append(soundAlbum.soundAlbum2dict())
        jsonValue = json.dumps(jsonArr)
        resp = Response(jsonValue, status=200, mimetype='application/json')
        return resp
    except Exception,e:
        print e.message
    finally:
        # 关闭session:
        session.close()

@app.route('/api/sound', methods=['GET'])
def api_get_sounds():
    album_id = request.args.get('album_id')
    count = request.args.get('count')
    page = request.args.get('page')
    if album_id == None:
        message = {
            'status': 41,
            'message': 'album_id参数为空',
        }
        jsonValue = json.dumps(message)
        resp = Response(jsonValue, status=200, mimetype='application/json')
        return resp
    if count == None:
        count = 20
    if page == None:
        page = 0
    #创建Session:
    session = DBSession()
    try:
        sounds = session.query(Sound).filter(Sound.in_albums.ilike('%{0}%'.format(album_id))).order_by(cast(Sound.id,INTEGER).desc()).slice(0+int(page)*int(count),int(count)+int(page)*int(count)).all()
        session.close()

        jsonArr = []
        for sound in sounds:
            jsonArr.append(sound.sound2dict())
        jsonValue = json.dumps(jsonArr)
        resp = Response(jsonValue, status=200, mimetype='application/json')
        return resp
    except Exception,e:
        print e.message
    finally:
        # 关闭session:
        session.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    # app.run(host='115.28.135.119',port=8989)
    app.run(host='127.0.0.1',port=8000)
