import copy
import pickle
import random
import threading

from pathlib import Path
from typing import List, Tuple

from constant import *


class QuadNode:
    _STORAGE_PATH = Path(__file__).parent / "quad_data.pkl"

    def __init__(self, cells, direct):
        self.cells = copy.deepcopy(list(cells))
        self.cells = sorted(self.cells)
        self.dir = direct

        self.neighbor : List[List[int]] = []
        self.is_valid = True

    def __hash__(self):
        return hash((tuple(self.cells), self.dir))

    def __eq__(self, other):
        return isinstance(other, QuadNode) and self.cells == other.cells

    def get_u(self):
        return min(c[0] for c in self.cells)
    def get_d(self):
        return max(c[0] for c in self.cells)
    def get_l(self):
        return min(c[1] for c in self.cells)
    def get_r(self):
        return max(c[1] for c in self.cells)
    # True:  垂直
    # False: 水平
    def get_space(self):
        if self.get_d() - self.get_u() >= 2:
            return True
        return False

    # 弯道是否连接
    def is_curve_close(self, other):

        # 最多一个节点不同
        cell_set = set(self.cells)
        for cell in other.cells:
            cell_set.add(cell)
        if len(cell_set) != 5:
            return False


        # 不同的节点不能跳格
        c1 = c2 = (0, 0)
        for c in cell_set:
            if c not in other.cells:
                c1 = c
            if c not in self.cells:
                c2 = c
        if abs(c1[0] - c2[0]) >= 2 or abs(c1[1] - c2[1]) >= 2:
            return False


        # 方向检测
        # 1.水平垂直切换
        dir_diff = 1 if self.dir != other.dir else -1
        if self.get_space() != other.get_space():
            if other.get_space():
                if (c2[1] - c1[1]) * other.dir < 0:
                    return False
            if not other.get_space():
                if (c2[0] - c1[0]) * other.dir > 0:
                    return False
        # 2.水平垂直不切换
        if self.get_space() == other.get_space():
            if self.dir != other.dir:
                return False


        if self.get_space():
            if (c2[1] - c1[1]) * self.dir < 0:
                return False
        if not self.get_space():
            if (c2[0] - c1[0]) * self.dir > 0:
                return False

        return True


    def is_horizontal(self):
        return self.cells[0][0] == self.cells[1][0] and self.cells[1][0] == self.cells[2][0] and self.cells[2][0] == self.cells[3][0]

    def is_vertical(self):
        return self.cells[0][1] == self.cells[1][1] and self.cells[1][1] == self.cells[2][1] and self.cells[2][1] == self.cells[3][1]

    @classmethod
    def save_to_file(cls, qnodes, qmap):
        """压缩存储节点数据"""
        with open(cls._STORAGE_PATH, 'wb') as f:
            pickle.dump({'nodes': qnodes, 'map': qmap}, f)

    @classmethod
    def load_from_file(cls):
        """从文件加载节点数据"""
        try:
            with open(cls._STORAGE_PATH, 'rb') as f:
                data = pickle.load(f)
                return data['nodes'], data['map']
        except FileNotFoundError:
            return None, None

    @classmethod
    def data_exists(cls):
        """检查数据文件是否存在"""
        return cls._STORAGE_PATH.exists()


def get_quad():
    # 直接从缓存中取
    if QuadNode.data_exists():
        quad_nodes, quad_map = QuadNode.load_from_file()

        if CONST_NEED_UPDATE:
            # 更新一下常量修改
            for i in range(len(quad_nodes)):
                for k in range(len(quad_nodes[i].neighbor)):
                    j, _ = quad_nodes[i].neighbor[k]
                    if quad_nodes[i].is_curve_close(quad_nodes[j]):
                        quad_nodes[i].neighbor[k][1] = CURVE_DISTANCE
                        continue
                    quad_nodes[i].neighbor[k][1] = STRAIGHT_DISTANCE
            # 保存到文件缓存
            QuadNode.save_to_file(quad_nodes, quad_map)

        return quad_map, quad_nodes

    quad_nodes = []
    quad_map = dict()

    def add_node(node_):
        if quad_map.get(node_) is None:
            quad_map[node_] = len(quad_nodes)
            quad_nodes.append(node_)

    def add_edge(node_1, node_2, dist):
        if quad_map.get(node_1) is None or quad_map.get(node_2) is None:
            return
        quad_nodes[quad_map[node_1]].neighbor.append([quad_map[node_2], dist])

    # 建节点
    for x in range(MAP_ROWS):
        for y in range(MAP_COLS):
            cells_set = [*node_search(x, y, -1), *node_search(x, y, 1)]
            for cells in cells_set:
                add_node(QuadNode(cells, 1))
                add_node(QuadNode(cells, -1))

    # 建边
    # 1.弯道边
    for i in range(0, len(quad_nodes)):
        node0 = quad_nodes[i]

        close_set = set()
        node0_set = set(node0.cells)
        for j in range(4):
            cell = node0.cells[j]
            for dx, dy in DIA_DIRECTIONS:
                next_x = cell[0] + dx
                next_y = cell[1] + dy
                if 0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and (next_x, next_y) not in node0_set:
                    close_set.add((next_x, next_y, j))

        for next_x, next_y, j in close_set:
            close_node = copy.deepcopy(node0)
            close_node.cells[j] = (next_x, next_y)
            close_node.cells = sorted(close_node.cells)

            close_node.dir = 1
            if node0.is_curve_close(close_node):
                add_edge(node0, copy.deepcopy(close_node), CURVE_DISTANCE)

            close_node.dir = -1
            if node0.is_curve_close(close_node):
                add_edge(node0, copy.deepcopy(close_node), CURVE_DISTANCE)

    # 2.直线边
    for i in range(0, len(quad_nodes)):
        node0 = quad_nodes[i]
        if node0.is_vertical():
            node1 = QuadNode([(node0.cells[0][0], node0.cells[0][1] + node0.dir),
                              (node0.cells[1][0], node0.cells[1][1] + node0.dir),
                              (node0.cells[2][0], node0.cells[2][1] + node0.dir),
                              (node0.cells[3][0], node0.cells[3][1] + node0.dir)], node0.dir)
            add_edge(node0, node1, STRAIGHT_DISTANCE)
        if node0.is_horizontal():
            node1 = QuadNode([(node0.cells[0][0] - node0.dir, node0.cells[0][1]),
                              (node0.cells[1][0] - node0.dir, node0.cells[1][1]),
                              (node0.cells[2][0] - node0.dir, node0.cells[2][1]),
                              (node0.cells[3][0] - node0.dir, node0.cells[3][1])], node0.dir)
            add_edge(node0, node1, STRAIGHT_DISTANCE)

    # 打乱边的顺序，让路径看起来更随机
    for i in range(len(quad_nodes)):
        random.shuffle(quad_nodes[i].neighbor)

    #保存到文件缓存
    QuadNode.save_to_file(quad_nodes, quad_map)

    return quad_map, quad_nodes


# 把四元点往某个方向搜出来
def node_search(x, y, x_dir):
    cells_set = []
    for masks in range(1 << 4):
        nx, ny = x, y
        cells = []
        for i in range(4):
            if nx >= MAP_ROWS or ny >= MAP_COLS or nx < 0 or ny < 0:
                break
            cells.append((nx, ny))
            if (masks >> i) & 1: nx += x_dir
            else: ny += 1

        if len(cells) == 4:
            cells_set.append(cells)

    return cells_set