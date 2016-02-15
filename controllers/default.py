# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def index():
    images = db().select(db.image.ALL, orderby=db.image.x|db.image.y)
    return dict(images=images)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def insert():
    db.users.insert(token=request.args[0],name=request.args[1])
    return

#from PIL import Image
import urllib2
from StringIO import StringIO
def my_form_processing(form):
    try:
        r = urllib2.urlopen(form.vars.url)
        im = Image.open(StringIO(r.read()))
        width, height = im.size
        form.vars.height = height
        form.vars.width = width
        session.flash = form.vars.url
    except:
       form.errors.b = 'Image url invalid'

@auth.requires_login()
def display_form():
   form = SQLFORM(db.images)
   if form.process(onvalidation=my_form_processing).accepted:
       session.flash = 'record inserted'
       #redirect(URL())
   elif form.errors:
        response.flash = 'form has errors'
   else:
        response.flash = 'please fill the form'
   return dict(form=form)

def deleteimage(user, imageid):
    db((db.images.id == imageid) & (db.images.user_id == user)).delete()
    return

def add():
    form = SQLFORM(db.image)
    if form.process().accepted:
        response.flash='new picture added'
    return dict(form=form)

def flag():
    db.flagged.insert(image_id=request.args[0])
    return
