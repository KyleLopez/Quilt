# -*- coding: utf-8 -*-
# try something like
panel_rows = 4
panel_columns = 4
height = width = 100


def Panel():
    return dict(quilt_column=request.vars['col'],
                 panel_rows=panel_rows,
                 panel_columns=panel_columns,
                 height=height,
                 width=width)

def Quilt():
    return dict(quilt_row=request.vars['row'])
