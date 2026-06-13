import pygame as pg
import pygame_menu
from settings import *

from glass.main import Model as GlassModel
from timelapse.main import Model as TimelapseModel
from tunnelle import Tunnele1, Tunnele2
from panic_rect.main import Model as PanicModel
from car.main import Model as CarModel
def run_glass():
    GlassModel(screen).main_loop()

def run_time_lapse():
    TimelapseModel(screen).main_loop()

def run_tunnele(version):
    if version == 1:
        Tunnele1(screen).main_loop()
    elif version == 2:
        Tunnele2(screen).main_loop()

def run_paniker():
    PanicModel(screen).main_loop()

def run_car():
    CarModel(screen).main_loop()


def make_tunnele_sub_menu():

    tunnelle_menu = pygame_menu.Menu('Тоннель', SCREEN_WIDTH, SCREEN_HEIGHT)
    tunnelle_menu.add.label("Светлый")
    tunnelle_menu.add.label("(Пробел - погасить тоннель)")
    tunnelle_menu.add.button('Запуск', lambda: run_tunnele(1))
    tunnelle_menu.add.label('')
    tunnelle_menu.add.label("Тёмный")
    tunnelle_menu.add.label("(Пробел - создать гейт)")
    tunnelle_menu.add.button('Запуск', lambda: run_tunnele(2))
    tunnelle_menu.add.button('Назад', pygame_menu.events.BACK)

    return tunnelle_menu
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Эксперименты")
    main_menu = pygame_menu.Menu('Меню', SCREEN_WIDTH, SCREEN_HEIGHT)
    main_menu.add.button('Стекло', run_glass)
    main_menu.add.button('Таймлапс', run_time_lapse)
    main_menu.add.button("Тоннель", make_tunnele_sub_menu())
    main_menu.add.button("Паникёр", run_paniker)
    main_menu.add.button("Машинка", run_car)

    main_menu.add.button('Выход', pygame_menu.events.EXIT)
    main_menu.mainloop(screen)
