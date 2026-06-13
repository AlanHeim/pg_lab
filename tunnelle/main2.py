import pygame as pg
from settings import *




class Gate:
    first = None
    tunnele = set()
    def __init__(self, size: tuple[int, int], color=(255, 255, 255), parent=None):
        self.rect = pg.Rect(0, 0, *size)
        gradient = max(0, 255 - len(self.tunnele) * 5)
        self.color = (gradient, gradient, gradient)
        self.speed = 1 + len(self.tunnele) // 3
        self.board_width = max(1, 4 - len(self.tunnele) // 3)
        self.parent: pg.Rect = parent.rect if parent else self.screen.get_rect()
        self.rect.center = self.parent.center


        self.kid = None

    @classmethod
    def grow_deep(cls):
        if cls.first:
            cls.first.grow()
        else:
            cls.first = Gate((SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.9))
            cls.tunnele.add(cls.first)
    @classmethod
    def init_screen(cls, screen):
        cls.screen = screen
    @classmethod
    def update_all(cls):
        if cls.first:
            cls.first.update()

    @classmethod
    def show(cls):
        if cls.first:
            cls.first.draw()


    def grow(self):
        if self.kid:
            self.kid.grow()
        else:
            self.kid = Gate((self.rect.width * 0.9, self.rect.height * 0.9), parent=self)
            self.tunnele.add(self.kid)
    def update(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.rect.center

        if x < mouse_x:
            if self.rect.right < self.parent.right:
                self.rect.right += self.speed
            else:
                self.parent.right += self.speed
        elif x > mouse_x:
            if self.rect.left > self.parent.left:
                self.rect.left -= self.speed
            else:
                self.parent.left -= self.speed

        if y < mouse_y:
            if self.rect.bottom < self.parent.bottom:
                self.rect.bottom += self.speed
            else:
                self.parent.bottom += self.speed
        elif y > mouse_y:
            if self.rect.top > self.parent.top:
                self.rect.top -= self.speed
            else:
                self.parent.top -= self.speed

        if self.kid:
            self.kid.update()


    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect, self.board_width)
        if self.kid:
            self.kid.draw()


class Model:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        Gate.init_screen(self.screen)

    def main_loop(self):
        Gate.first = None
        Gate.tunnele.clear()


        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    Gate.grow_deep()

            self.screen.fill((0, 0, 0))
            if Gate.tunnele:
                Gate.update_all()
                Gate.show()

            pg.display.flip()
            self.clock.tick(FPS)



