import pygame as pg
from settings import SCREEN_HEIGHT

pg.font.init()

font_adaptive = pg.font.Font(None, int(SCREEN_HEIGHT * 0.07))
font_30 = pg.font.SysFont("Arial", 30)


def make_text_label(text, text_color="black", bg_color=None, font=0):
    """font - размер шрифта"""

    if font == 0:
        font = font_adaptive
    elif font == 30:
        font = font_30
    return font.render(text, True, text_color, bg_color)