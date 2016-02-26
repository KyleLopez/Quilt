#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def makeThumbnail(db, request, dbtable,ImageID,size=(150,150)):
    try:
        thisImage=db(dbtable.id==ImageID).select()[0]
        import os, uuid
        from PIL import Image
    except: return
    ima=Image.open(request.folder + 'uploads/' + thisImage.im)
    ima.thumbnail(size,Image.ANTIALIAS)
    thumbName='image.thumb.%s.jpg' % (uuid.uuid4())
    ima.save(request.folder + 'uploads/' + thumbName,'jpeg')
    thisImage.thumb=thumbName
    thisImage.update_record()
    return
