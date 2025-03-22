import copy
from typing import List, Union, Dict

import DataSearch.service as data_service
from Map.Algorithm.Gener import Gener

from Map.Algorithm.Parker.QuadNode import get_all_quad_nodes, QuadNode
from Map.constant import *


class Parker:
    def __init__(self, map0, entry, target):
        self.map0 = map0
        self.map1 = copy.deepcopy(map0)
        self.carPos = None
        # 获取所有四元节点
        self.quad_map, self.quad_nodes = get_all_quad_nodes()
        self.start = self.quad_map[QuadNode(entry)]

        self.end : List[Union[int, None]] = [None, None]
        self.find_end(target)
        # 处理和障碍物的距离限制
        for x in range(MAP_ROWS):
            for y in range(MAP_COLS):
                if self.map1[x][y] != 'empty' and self.map1[x][y] != 'free':
                    continue
                for dx, dy in DIRECTIONS:
                    next_y = y + dy
                    next_x = x + dx
                    # 检查边界和可通行性
                    if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                            self.map1[next_x][next_y] == 'occupy'):
                        self.map1[x][y] = 'close'

        for i in range(len(self.quad_nodes)):
            self.quad_nodes[i].is_valid = True
            for cell in self.quad_nodes[i].cells:
                if self.map1[cell[0]][cell[1]] not in ('free', 'entry', 'empty'):
                    self.quad_nodes[i].is_valid = False
                    break

        print("Parker init done")


    def bfs(self, end) -> Union[List[QuadNode], None]:
        if end is None:
            return None
        path : List[QuadNode] = []
        queue = [self.start]
        visited : Dict[int, Union[int, None]] = {self.start: None}
        found = False
        current : Union[int, None] = None

        while queue and not found:
            current = queue.pop(0)
            # 到达目标点
            if current == end:
                found = True
                break
            for neighbor in self.quad_nodes[current].neighbor:
                if self.quad_nodes[neighbor].is_valid and neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        if found:
            while current:
                path.append(self.quad_nodes[current])
                current = visited[current]
            path.reverse()
            return path

        return None


    def find_path(self) -> Union[List[QuadNode], None]:
        all_path = []
        for end in self.end:
            all_path.append(self.bfs(end))

        path = None
        for p in all_path:
            if p is not None:
                if path is None or len(p) < len(path):
                    path = p
        return path


    def find_end(self, target):
        # 处理目标节点
        all_ps = data_service.get_car_positions()
        for p_ in all_ps:
            if (p_.LU_x_coord <= target[0] <= p_.RD_x_coord and
                    p_.LU_y_coord <= target[1] <= p_.RD_y_coord):
                self.carPos = p_
                for i in range(p_.LU_x_coord, p_.RD_x_coord + 1):
                    for j in range(p_.LU_y_coord, p_.RD_y_coord + 1):
                        self.map1[i][j] = 'free'
                break

        p = self.carPos
        if p.RD_x_coord - p.LU_x_coord == 3:
            self.end[0] = self.quad_map[QuadNode([(p.LU_x_coord, p.LU_y_coord),
                                  (p.LU_x_coord + 1, p.LU_y_coord),
                                  (p.LU_x_coord + 2, p.LU_y_coord),
                                  (p.LU_x_coord + 3, p.LU_y_coord)])]
            self.end[1] = self.quad_map[QuadNode([(p.LU_x_coord, p.RD_y_coord),
                                  (p.LU_x_coord + 1, p.RD_y_coord),
                                  (p.LU_x_coord + 2, p.RD_y_coord),
                                  (p.LU_x_coord + 3, p.RD_y_coord)])]
        if p.RD_y_coord - p.LU_y_coord == 3:
            self.end[0] = self.quad_map[QuadNode([(p.LU_x_coord, p.LU_y_coord),
                                  (p.LU_x_coord, p.LU_y_coord + 1),
                                  (p.LU_x_coord, p.LU_y_coord + 2),
                                  (p.LU_x_coord, p.LU_y_coord + 3)])]
            self.end[1] = self.quad_map[QuadNode([(p.RD_x_coord, p.LU_y_coord),
                                  (p.RD_x_coord, p.LU_y_coord + 1),
                                  (p.RD_x_coord, p.LU_y_coord + 2),
                                  (p.RD_x_coord, p.LU_y_coord + 3)])]