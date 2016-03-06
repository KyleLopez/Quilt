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

def show_image():
    image_id = request.args[0]
    image = db(db.image.id==image_id).select().first()
    return dict(image=image)

import bleach

def show_image_ajax():
    if not request.args:
        raise HTTP(400)
    image_id = request.args[0]
    image = db(db.image.id==image_id).select().first()
    comments = db(db.comments.image_id==image_id).select()
    form = SQLFORM(db.comments, fields = ['body'])
    form.vars.image_id = image_id
    if form.process().accepted:
        text = form.vars.body
        row = db(db.comments.id==form.vars.id).select().first()
        row.update_record(body=bleach.clean(text))
        redirect(URL('default', 'show_image_ajax', args=image_id), client_side=True)
    return dict(image=image, comments=comments, form=form)

@auth.requires_login()
def confirmdelete():
    if not request.args:
        raise HTTP(400)
    #try:
    imageid = request.args[0]
    if db((db.images.id == imageid) & (db.images.user_id == auth.user_id)).isempty():
        redirect(URL('static', 'nopermissions'))
    db((db.images.id == imageid) & (db.images.user_id == auth.user_id)).delete()
    redirect(URL('static', 'success'))
    #except:
    #    raise HTTP(401)
    return dict()

def addtag():
    if not request.args:
        raise HTTP(400)
    imageid = request.args[0]
    form = SQLFORM(db.image_tags)
    text = ""
    if form.process().accepted:
        session.flash =  form.vars.tag
        text = form.vars.tag
        row = db(db.image_tags.id==form.vars.id).select().first()
        row.update_record(tag=bleach.clean(text).lower())
        row.update_record(image_id=imageid)
    elif form.errors:
        response.flash = 'Tag has errors'
    else:
        response.flash = 'Enter your tag'
    return dict(form=form)

#@auth.requires_login()
def addcomment():
    if not request.args:
        raise HTTP(400)
    imageid = request.args[0]
    form = SQLFORM(db.comments)
    text = ""
    if form.process().accepted:
        text = form.vars.body
        row = db(db.comments.id==form.vars.id).select().first()
        row.update_record(body=bleach.clean(text))
        row.update_record(image_id=imageid)
    elif form.errors:
        response.flash = 'Comment has errors'
    else:
        response.flash = 'Enter your comment'
    return dict(form=form)
