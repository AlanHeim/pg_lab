import pygame as pg
from settings import *


class Model:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True

    def main_loop(self):

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            pg.display.flip()
            self.clock.tick(FPS)
