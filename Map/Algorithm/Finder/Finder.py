import copy
import random
from typing import Dict, Tuple, Union, List

import DataSearch.service as data_service

from constant import *

class Finder:
    def __init__(self, map0, start, end):
        # 实际赋值
        self.map0 = map0
        self.map1 = copy.deepcopy(map0)
        self.directions = DIRECTIONS

        self.start, self.end = start, end

        # 在路径搜索前处理目标停车位
        all_ps = data_service.get_car_positions()

        for p in all_ps:
            # 检查目标点是否在该停车位范围内
            if (p.LU_x_coord <= end[0] <= p.RD_x_coord and
                    p.LU_y_coord <= end[1] <= p.RD_y_coord):
                self.carPos = p
                for i in range(p.LU_x_coord, p.RD_x_coord + 1):
                    for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                        self.map1[i][j] = 'free'
                break

        # 处理和障碍物的距离限制
        for x in range(MAP_ROWS):
            for y in range(MAP_COLS):
                if self.map1[x][y] != 'empty':
                    continue
                for dx, dy in self.directions:
                    next_y = y + dy
                    next_x = x + dx
                    # 检查边界和可通行性
                    if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                            self.map1[next_x][next_y] == 'occupy'):
                        self.map1[x][y] = 'close'


    def find_path(self) -> Union[List[Tuple[int, int]], None]:
        path : List[Tuple[int, int]] = []
        queue = [self.start]
        visited: Dict[Tuple[int, int], Union[Tuple[int, int], None]] = {self.start: None}
        found = False
        current : Union[Tuple[int, int], None] = None

        while queue and not found:
            current = queue.pop(0)
            # 到达目标点
            if current == self.end:
                found = True
                break

            random.shuffle(self.directions)  # 每次请求随机打乱方向顺序
            for dx, dy in self.directions:
                next_x = current[0] + dx
                next_y = current[1] + dy
                # 检查边界和可通行性
                if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                        (next_x, next_y) not in visited and
                        self.map1[next_x][next_y] in ('free', 'entry', 'empty')):
                    visited[(next_x, next_y)] = current
                    queue.append((next_x, next_y))

        # 回溯路径
        if found:
            while current:  # 此时current已明确绑定
                path.append(current)
                current = visited[current]
            return path

        return None

    def inside(self, x, y) -> bool:
        p = self.carPos
        return p.LU_x_coord <= x <= p.RD_x_coord and p.LU_y_coord <= y <= p.RD_y_coord
