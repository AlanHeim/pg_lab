from math import sin, cos, radians
import pygame as pg
from settings import *
from tools import make_text_label


class Car(pg.sprite.Sprite):
    __size: tuple[int, int] = (20, 40)  # размер
    __base_body = pg.surface.Surface(__size, pg.SRCALPHA)
    __base_body.fill("black")
    pg.draw.rect(__base_body, "blue", (0, 0, 20, 10))

    def __init__(self, where=None):
        pg.sprite.Sprite.__init__(self)
        self.image = self.__base_body
        if where is None:
            where = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.rect = self.image.get_rect(center=where)

        self.rotated_image = self.image
        self.rotated_rect = self.rect

        self.rotation_angle = 0
        self.rotation_speed = 2



    def update(self):

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.rotation_angle -= self.rotation_speed
        elif keys[pg.K_a]:
            self.rotation_angle += self.rotation_speed

        if keys[pg.K_w]:
            self.rect.x -= 10 * sin(radians(self.rotation_angle))
            self.rect.y -= 10 * cos(radians(self.rotation_angle))
        elif keys[pg.K_s]:
            self.rect.x += 10 * sin(radians(self.rotation_angle))
            self.rect.y += 10 * cos(radians(self.rotation_angle))

        if keys[pg.K_e]:
            self.rect.x += 10 * cos(radians(self.rotation_angle))
            self.rect.y -= 10 * sin(radians(self.rotation_angle))
        elif keys[pg.K_q]:
            self.rect.x -= 10 * cos(radians(self.rotation_angle))
            self.rect.y += 10 * sin(radians(self.rotation_angle))

        self.rotated_image = pg.transform.rotate(self.image, self.rotation_angle)

        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rotated_rect)



class Model:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.car = Car()
    def draw_hints(self):
        hints = ["W/S - вперёд/назад",
                 "A/D - против/по часовой",
                 "Q/D - скачок влево/вправо"]
        x, y = 10, 10
        for hint in hints:
            text = make_text_label(hint, True )
            self.screen.blit(text, (x, y))
            y += 30
    def main_loop(self):

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.car.update()

            self.screen.fill("white")
            self.car.draw(self.screen)
            self.draw_hints()

            pg.display.flip()
            self.clock.tick(FPS)
