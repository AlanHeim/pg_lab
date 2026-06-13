from random import randint
import pygame as pg
from settings import *



class Gate:
    def __init__(self, screen: pg.Surface, color, step):
        self.screen = screen
        self.color = color
        self.step = step
        self.screen_width, self.screen_height = screen.get_size()
        self.gate = pg.Surface((self.screen_width * 0.9, self.screen_height * 0.9), pg.SRCALPHA)
        self.gate_rect = self.gate.get_rect()

    def __scale_coords(self, coord):
        x, y = coord
        for i in range(self.step):
            x /= 0.9
            y /= 0.9
        return (int(x), int(y))

    def update(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.__scale_coords(self.gate_rect.center)

        if x < mouse_x:
            if self.gate_rect.right < self.screen_width:
                self.gate_rect.right += 1
        elif x > mouse_x:
            if self.gate_rect.left > 0:
                self.gate_rect.left -= 1

        if y < mouse_y:
            if self.gate_rect.bottom < self.screen_height:
                self.gate_rect.bottom += 1
        elif y > mouse_y:
            if self.gate_rect.top > 0:
                self.gate_rect.top -= 1

    def _update_color(self):
        self.gate.fill(self.color)

    def turn_off(self):
        self.color = (0, 0, 0, 255)

    def draw(self):

        self.screen.blit(self.gate, self.gate_rect)
        self._update_color()


def random_color():
    color = []
    for i in range(3):
        color.append(randint(0, 255))
    return tuple(color)


def make_tunnel(screen, x):
    gates = []
    current_surface = screen
    for i in range(x):
        gate = Gate(current_surface, (100, 100, 100, 20), i)
        gates.append(gate)
        current_surface = gate.gate

    return gates
class Model:
    def __init__(self, screen):

        self.screen = screen
        self.clock = pg.time.Clock()
        self.tunnel = make_tunnel(screen, 200)

        self.tunnel.reverse()
        self.screen_color = "white"
        self.darkness = False
        self.dark_index = 0
        self.running = True
    def main_loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.darkness = True

            if self.darkness:
                if self.dark_index < len(self.tunnel):
                    self.tunnel[self.dark_index].turn_off()
                    self.dark_index += 1
                else:
                    self.screen_color = "black"
                    self.darkness = False

            self.screen.fill(self.screen_color)
            for gate in self.tunnel:
                gate.update()
                gate.draw()

            pg.display.flip()
            self.clock.tick(FPS)




