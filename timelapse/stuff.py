class Time:
    _dark = 0
    _light = 720

    def __init__(self, now=0, rise=True):
        self.now = now
        self.rise = True

    def go(self):
        while True:
            if self.rise:
                self.now += 1
                if self.now >= self._light:
                    self.rise = False
            else:
                self.now -= 1
                if self.now <= self._dark:
                    self.rise = True
            yield self.now


class Sky:
    r = 0
    g = 0
    b = 0

    # 135, 206, 235 цвет дневного неба

    def _update(self, time: int):
        self.r = time // 5.3
        self.g = time // 3.4
        self.b = time // 3
        # коэффициент рассчитан делением времени самой светлой точки на интенсивность цвета

    def color(self, time):
        self._update(time)
        return self.r, self.g, self.b


class Sun:
    def __init__(self, rect, screen_size):
        self.rect = rect
        self.x_way = (-20, screen_size[0] + 20)
        self.x_path = self.x_way[1] + abs(self.x_way[0])

        self.y_way = (screen_size[1] + 20, screen_size[1] * 0.2)
        self.y_step = (self.y_way[0] - self.y_way[1]) / 100
        self.y = self.y_way[0]

    def get_pos(self, time: int, rise: bool):
        if rise:
            percent = time / 7.2
            x = percent * (self.x_path / 100)
            if x <= 20:
                x *= -1

            if x <= self.x_path // 2:
                self.y *= 0.99
            else:
                self.y *= 1.01
            y = self.y



        else:
            x = self.x_way[0]
            y = self.y_way[0]
        self.rect.center = (int(x), int(y))
