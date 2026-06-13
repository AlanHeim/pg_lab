import pygame as pg
from .stuff import *
from settings import *
from tools import make_text_label


class Model:
    def __init__(self, screen):

        self.screen = screen
        self.clock = pg.time.Clock()



        self.simulate_time = Time()
        self.mig = self.simulate_time.go()

        self.sky = Sky()
        self.sun = Sun(pg.Rect((0, SCREEN_SIZE[1] + 20, 20, 20)), SCREEN_SIZE)

        self.running = True
    def main_loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            now = next(self.mig)
            text = make_text_label(str(now), "white")

            self.screen.fill(self.sky.color(now))
            self.screen.blit(text, (10, 10))
            self.sun.get_pos(now, self.simulate_time.rise)
            pg.draw.circle(self.screen, "yellow", self.sun.rect.center, 10)

            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    model = Model(pg.display.set_mode(SCREEN_SIZE))
    model.main_loop()
