# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def index():
    return dict()

def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()

def insert():
    db.users.insert(token=request.args[0],name=request.args[1],ip_add=request.client)
    return

def deleteimage(user, imageid):
    db((db.images.id == imageid) & (db.images.user_id == user)).delete()
    return

import os
import math
from PIL import Image
def add():
    form = SQLFORM(db.image, hidden={'ip_add':request.client})
    form.vars.x = request.args(0,cast=int)
    form.vars.y = request.args(1,cast=int)
    if form.process().accepted:
        maxsize = 1080
        im = form.vars.im
        image = Image.open(os.path.join(request.folder, 'uploads',  im))
        width, height = image.size
        if width > maxsize or height > maxsize:
            ratio = width/float(height)
            size = (int(math.ceil(ratio*maxsize)), maxsize)
            if width >= height:
                ratio = height/float(width)
                size = (maxsize, int(math.ceil(ratio*maxsize)))
            im_location = os.path.join(request.folder, 'uploads',  im)
            image.resize(size, Image.ANTIALIAS).save(im_location)
        response.flash='new picture added'
        redirect(URL('index'))
    return dict(form=form)

def flag():
    db.flagged.insert(image_id=request.args[0])
    return

def unflag():
    image_id = request.args[0]
    db(db.flagged.image_id==image_id).delete()
    return

import bleach

def show_image_ajax():
    if not request.args:
        raise HTTP(400)
    image_id = request.args[0]
    image = db(db.image.id==image_id).select().first()
    tags = db(db.image_tags.image_id==image_id).select(db.image_tags.tag, distinct=True)
    return dict(image=image, tags=tags)

def confirmdelete():
    if not request.args:
        raise HTTP(400)
    #try:
    imageid = request.args[0]
    if db((db.image.id == imageid) and (db.image.ip_add == "|" + request.client + "|")).isempty():
        return dict(message="You do not have permissions to delete this image")
    db((db.image.id == imageid) and (db.image.ip_add == "|" + request.client + "|")).delete()
    #except:
    #    raise HTTP(401)
    return dict(message="Success")

def addtag():
    if not request.args:
        raise HTTP(400)
    imageid = request.args[0]
    form = SQLFORM(db.image_tags)
    form.vars.image_id=imageid
    text = ""
    if form.process().accepted:
        session.flash =  form.vars.tag
        text = form.vars.tag
        row = db(db.image_tags.id==form.vars.id).select().first()
        row.update_record(tag=bleach.clean(text).lower())
        redirect(URL('default', 'show_image_ajax', args=imageid))
    elif form.errors:
        response.flash = 'Tag has errors'
    else:
        response.flash = 'Enter your tag'
    return dict(form=form)

def tagged():
    if not request.args:
        raise HTTP(400)
    tag = request.args[0]
    images = db(db.image_tags.tag==tag).select(db.image_tags.image_id, distinct=True)
    return dict(images=images)
