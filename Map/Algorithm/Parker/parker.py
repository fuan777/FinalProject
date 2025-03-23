import copy
import heapq
from typing import List, Union, Dict

import DataSearch.service as data_service

from Map.Algorithm.Parker.quad_node.builder import get_quad, QuadNode
from Map.Algorithm.algorithm import dijkstra
from constant import *


class Parker:
    def __init__(self, map0, entry, target):
        self.map0 = map0
        self.map1 = copy.deepcopy(map0)
        self.car_pos = None
        print("##start get quad##")
        # 获取所有四元节点
        self.quad_map, self.quad_nodes = get_quad()

        self.start = self.quad_map[QuadNode(entry, 1)]
        self.end : List[int] = []
        self.find_end(target)

        self.init_limit()
        # 检测 4元格点 合法性
        self.init_valid()
        print("Parker init done")

    def init_limit(self):
        # 处理和障碍物的距离限制，Parking两圈不能有障碍物，Finding一圈
        for x in range(MAP_ROWS):
            for y in range(MAP_COLS):
                if self.map1[x][y] in ('occupy', 'border'):
                    continue
                # 第一圈
                range1 = []
                for dx, dy in DIRECTIONS:
                    next_y = y + dy
                    next_x = x + dx
                    # 检查边界和可通行性
                    if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                            self.map1[next_x][next_y] in ('occupy', 'border')):
                        self.map1[x][y] = 'close'
                        break
                    range1.append((next_x, next_y))
                # 第二圈
                for x1, y1 in range1:
                    for dx, dy in DIRECTIONS:
                        next_y = y1 + dy
                        next_x = x1 + dx
                        # 检查边界和可通行性
                        if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                                self.map1[next_x][next_y] in ('occupy', 'border')):
                            self.map1[x][y] = 'close'
                            break

    def init_valid(self):
        for i in range(len(self.quad_nodes)):
            self.quad_nodes[i].is_valid = True
            for cell in self.quad_nodes[i].cells:
                if self.map1[cell[0]][cell[1]] not in ('free', 'entry', 'empty'):
                    self.quad_nodes[i].is_valid = False
                    break

    def find_path(self) -> Union[List[QuadNode], None]:
        return dijkstra(self.quad_nodes, self.map1, self.start, self.end)

    def find_end(self, target):
        # 处理目标节点
        all_ps = data_service.get_car_positions()
        for p_ in all_ps:
            if (p_.LU_x_coord <= target[0] <= p_.RD_x_coord and
                    p_.LU_y_coord <= target[1] <= p_.RD_y_coord):
                self.car_pos = p_
                for i in range(p_.LU_x_coord, p_.RD_x_coord + 1):
                    for j in range(p_.LU_y_coord, p_.RD_y_coord + 1):
                        self.map1[i][j] = 'free'
                break

        p = self.car_pos
        if p.RD_x_coord - p.LU_x_coord == 3:
            for y in (p.LU_y_coord, p.RD_y_coord):
                for d in (1, -1):
                    cells = []
                    for i in range(4):
                        cells.append((p.LU_x_coord + i, y))
                    self.end.append(self.quad_map[QuadNode(cells, d)])

        if p.RD_y_coord - p.LU_y_coord == 3:
            for x in (p.LU_x_coord, p.RD_x_coord):
                for d in (1, -1):
                    cells = []
                    for i in range(4):
                        cells.append((x, p.LU_y_coord + i))
                    self.end.append(self.quad_map[QuadNode(cells, d)])