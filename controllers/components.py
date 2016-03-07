# -*- coding: utf-8 -*-
# try something like
panel_rows = 4
panel_columns = 4
height = width = 100

def pad_images(image_rows):
    n_image_rows = []
    for row in image_rows:
        n_image_rows.append(row)
    n_image_rows.append(None)
    return n_image_rows

def Panel():
    start_row = int(request.vars['row']) * panel_rows
    start_col = int(request.vars['col']) * panel_columns
    images = db((db.image.x >= start_row) & (db.image.x < start_row + panel_rows) &
                (db.image.y >= start_col) & (db.image.y < start_col + panel_columns)).select(db.image.ALL, orderby=db.image.x|db.image.y)
    if (len(images) < panel_rows * panel_columns):
        images = pad_images(images)
    return dict(panel_rows=panel_rows,
                 panel_columns=panel_columns,
                 row=start_row,
                 col=start_col,
                 height=height,
                 width=width,
                 images=images)

@cache.action()
def row():
    import math
    num_panels = math.ceil(float(request.vars['width']) / (panel_rows * width))
    return dict(quilt_row=request.args(0),panels=int(num_panels), panel_height=(panel_rows * height))

@cache.action()
def col():
    return dict(quilt_column=request.args(0), panel_width=(panel_columns * width))
