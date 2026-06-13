import pygame as pg
from settings import *


class Paniker(pg.sprite.Sprite):
    __size = (20, 40)
    __look = 50

    indication = {"покой": "blue",
                  "паника": "red"}

    __base_body = pg.surface.Surface(__size)
    __base_body.fill("black")

    def __init__(self, model, x=SCREEN_SIZE[0] // 2, y=SCREEN_SIZE[1] // 2):
        pg.sprite.Sprite.__init__(self)
        self.image = Paniker.__base_body
        self.rect = self.image.get_rect(center=(x, y))

        self.mode = "покой"
        self.model = model

    @property
    def eye_color(self):
        return self.indication[self.mode]

    @property
    def __grounded(self):
        result = False
        opora: int = self.rect.bottom
        print(opora, self.model.platforms.keys())
        if opora in self.model.platforms:
            for place in self.model.platforms[opora]:
                a = place[0]
                b = place[1]
                if a < self.rect.centerx < b:
                    result = True
        return result

    def check(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.rect.centerx, self.rect.bottom
        close = 100
        mouse_close = abs(mouse_x - x) < close and abs(mouse_y - y) < close
        if self.__grounded and not mouse_close:
            self.mode = "покой"
        else:
            self.mode = "паника"

        pg.draw.rect(self.image, self.eye_color, (0, 0, 20, 10))  # цветовой индикатор

    def correction(self):
        if self.model.GRAVITY[0] and not self.__grounded:
            self.rect.bottom += self.model.GRAVITY[1]
            if self.rect.bottom > SCREEN_SIZE[1]:
                self.rect.bottom = SCREEN_SIZE[1]

    def move(self, speed=3):

        if self.mode == "паника":
            if self.__grounded:
                if self.rect.centerx < pg.mouse.get_pos()[0]:
                    self.rect.x -= speed
                else:
                    self.rect.x += speed

    def update(self):

        self.check()
        self.correction()
        self.move()
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Model:
    GRAVITY = (True, 1)   # платформы корректно работают только с гравитацией 1
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.platforms: dict[int, list[tuple[int, int]]] = {
            SCREEN_SIZE[1]: [(0, SCREEN_SIZE[0])],
            SCREEN_SIZE[1] // 2: [(0, int(SCREEN_SIZE[0] * 0.25)),
                                  (int(SCREEN_SIZE[0] * 0.75), SCREEN_SIZE[0])]
        }  # поверхности
        # {Y: [(X1, X2), (X1, X2)]   каждый вложенный кортеж - отдельная платформа на данном уровне Y


        self.paniker = Paniker(self)

    def draw_platforms(self):
        for level, platforms in self.platforms.items():
            for platform in platforms:
                pg.draw.line(self.screen, "white",
                             (platform[0], level), (platform[1], level), 4)
    def main_loop(self):

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.paniker.rect.center = event.pos

            self.paniker.update()

            self.screen.fill("brown")
            self.paniker.draw(self.screen)
            self.draw_platforms()

            pg.display.flip()
            self.clock.tick(FPS)
