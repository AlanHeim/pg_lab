from random import randint
import pygame as pg
from settings import *
from tools import make_text_label

class Sun:
    def __init__(self, screen,
                 real=True):
        self.screen = screen
        self.rays = 1
        self.ray_color = [255, 255, 255]
        self.real = real

        self.clean = True

    def make_lane(self, a, steps):

        dots = [a]
        next_dot = a

        # 0 < next_dot[0] < screen_size[0] or 0 < next_dot[1] < screen_size[1]   край
        sunsize = 30

        while abs(a[0] - next_dot[0]) < sunsize or abs(a[1] - next_dot[1]) < sunsize:
            x_max = randint(1, sunsize)
            if steps[2]:
                if steps[0]:
                    new_dot_x = next_dot[0] + randint(1, x_max)
                else:
                    new_dot_x = next_dot[0] - randint(1, x_max)
            else:
                new_dot_x = next_dot[0] + randint(-sunsize, sunsize)

            if not steps[2]:
                if steps[1]:
                    new_dot_y = next_dot[1] + randint(1, x_max)
                else:
                    new_dot_y = next_dot[1] - randint(1, x_max)
            else:
                new_dot_y = next_dot[1] + randint(-sunsize, sunsize)

            next_dot = (new_dot_x, new_dot_y)
            dots.append(next_dot)

        pg.draw.aalines(self.screen, self.ray_color, False, dots)

    def glass_atack(self, coords):
        for _ in range(self.rays):
            steps = (bool(randint(0, 1)),
                     bool(randint(0, 1)),
                     bool(randint(0, 1)))

            self.make_lane(coords, steps)
            if self.real:  # если реал, то рисуется линия-антагонист
                self.make_lane(coords, (not steps[0], not steps[1], not steps[2]))

    def draw(self):

        mouse_keys = pg.mouse.get_pressed()
        # if mouse_keys[0]:
        #     for _ in range(30):
        #         make_lane(pg.mouse.get_pos(), (randint(0, 1), False))

        if True in mouse_keys:
            self.glass_atack(pg.mouse.get_pos())
            if self.rays < 100:
                self.rays += 1
                if self.rays >= 100:
                    self.clean = False

            for _ in range(10):
                col = randint(0, 2)
                if mouse_keys[0]:
                    if self.ray_color[col] > 0:
                        self.ray_color[col] -= 1
                elif mouse_keys[2]:
                    if self.ray_color[col] < 255:
                        self.ray_color[col] += 1
        else:
            self.rays = 1


class Model:
    def __init__(self, screen):

        self.screen = screen  #pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.hint_label = make_text_label(
            "пробел - стазис | лкм - темнее | пкм - светлее | С - отрисовка подсказки",
            "white", "black"
        )
        self.hint_rect = self.hint_label.get_rect(centerx=SCREEN_WIDTH//2)
        self.show_hint = True

        self.sun = Sun(self.screen)

        self.running = True

    def event_check(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            # if event.type == pg.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         glass_atack(pg.mouse.get_pos(), x=100)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.sun.clean = not self.sun.clean
                elif event.key == pg.K_c:
                    self.show_hint = not self.show_hint

    def main_loop(self):
        while self.running:
            self.event_check(pg.event.get())

            if self.sun.clean:
                self.screen.fill("black")

            self.sun.draw()

            if self.show_hint:
                self.screen.blit(self.hint_label, self.hint_rect)

            pg.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    model = Model(pg.display.set_mode(SCREEN_SIZE))
    model.main_loop()
