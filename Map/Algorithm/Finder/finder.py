import copy

import DataSearch.service as data_service

from Map.Algorithm.algorithm import bfs

from constant import *

class Finder:
    def __init__(self, map0, start, end):
        # 实际赋值
        self.map1 = copy.deepcopy(map0)
        self.start, self.end = start, end

        p = get_car_pos(end)
        
        # 把整个车位先标为free
        for i in range(p.LU_x_coord, p.RD_x_coord + 1):
            for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                self.map1[i][j] = 'free'
        self.car_pos = p

        # 更新和障碍物距离保持限制
        self.init_limit()


    def find_path(self):
        return bfs(self.map1, self.start, [self.end])

    def is_inside(self, x, y) -> bool:
        p = self.car_pos
        return p.LU_x_coord <= x <= p.RD_x_coord and p.LU_y_coord <= y <= p.RD_y_coord

    def init_limit(self):
        for x in range(MAP_ROWS):
            for y in range(MAP_COLS):
                if self.map1[x][y] in ('occupy', 'border'):
                    continue
                for dx, dy in DIRECTIONS:
                    next_y = y + dy
                    next_x = x + dx
                    # 检查边界和可通行性
                    if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                            self.map1[next_x][next_y] == 'occupy'):
                        self.map1[x][y] = 'close'
                        break


def get_car_pos(end):
    all_ps = data_service.get_car_positions()
    for p in all_ps:
        # 检查目标点是否在该停车位范围内
        if (p.LU_x_coord <= end[0] <= p.RD_x_coord and
                p.LU_y_coord <= end[1] <= p.RD_y_coord):
            return p
