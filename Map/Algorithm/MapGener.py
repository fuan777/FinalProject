import copy

import DataSearch.service as data_service
import DataSearch.generate as gen

from constant import *

class MapGener:
    def __init__(self, map0):
        self.map0 = copy.copy(map0)

    def gen_random(self):
        gen.generate_map01(MAP_ROWS, MAP_COLS)

    def set_car_pos(self):
        all_ps = data_service.get_car_positions()
        for p in all_ps:
            for i in range(p.LU_x_coord, p.RD_x_coord + 1):
                for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                    if p.is_occupied:
                        self.map0[i][j] = 'occupy'
                    else:
                        self.map0[i][j] = 'free'

    def set_border(self, lx, rx, ly, ry):
        for i in range(lx, rx):
            for j in range(ly, ry):
                self.map0[i][j] = 'border'

    def set_entry(self, lx, rx, ly, ry):
        for i in range(lx, rx):
            for j in range(ly, ry):
                self.map0[i][j] = 'entry'