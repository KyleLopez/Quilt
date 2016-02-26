from gluon import *
from thumbnailer import makeThumbnail

def index(): return dict()

def showthumb():
    image_id = request.args[0]
    makeThumbnail(db, request, db.image, image_id, (150, 150))
    image = db(db.image.id==image_id).select().first()
    return dict(image=image)
