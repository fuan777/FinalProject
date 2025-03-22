import copy
import pickle
import random
import threading

from pathlib import Path
from typing import List, Tuple

from Map.constant import *

'''缓存在程序中'''


class QuadNode:
    _STORAGE_PATH = Path(__file__).parent / "quad_data.pkl"

    def __init__(self, cells):
        self.cells = copy.deepcopy(cells)
        self.cells = sorted(self.cells)
        self.neighbor : List[Tuple[int, int]] = []
        self.is_valid = True

    def __hash__(self):
        h = 0
        for x, y in self.cells:
            h ^= (x << 16) + y
            h = (h * 0x9e3779b9) & 0xFFFFFFFF
        return h

    def __eq__(self, other):
        return isinstance(other, QuadNode) and self.cells == other.cells


    def is_close(self, other):
        cell_set = set(self.cells)
        for cell in other.cells:
            cell_set.add(cell)
        return len(cell_set) == 5

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

def get_all_quad_nodes():
    if QuadNode.data_exists():
        quad_nodes, quad_map = QuadNode.load_from_file()
        return quad_map, quad_nodes

    quad_nodes = []
    quad_map = dict()
    # 建节点
    for x in range(TEST_MAP_ROWS):
        for y in range(TEST_MAP_COLS):
            cells_set = [*node_search(x, y, -1), *node_search(x, y, 1)]
            for cells in cells_set:
                node = QuadNode(cells)
                if quad_map.get(node) is None:
                    quad_map[node] = len(quad_nodes)
                    quad_nodes.append(node)

    # 建边
    def add_edge_task(left_id, right_id):
        # 弯道边
        for i in range(left_id, right_id):
            node0 = quad_nodes[i]

            close_set = set()
            node0_set = set(node0.cells)
            for j in range(4):
                cell = node0.cells[j]
                node0_set.remove(cell)
                for dx, dy in DIA_DIRECTIONS:
                    next_x = cell[0] + dx
                    next_y = cell[1] + dy
                    if 0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and (next_x, next_y) not in node0_set:
                        close_set.add((next_x, next_y, j))
                node0_set.add(cell)

            for next_x, next_y, j in close_set:
                close_node = copy.deepcopy(node0)
                close_node.cells[j] = (next_x, next_y)

                if node0.is_close(close_node) and quad_map.get(close_node):
                    quad_nodes[i].neighbor.append((quad_map[close_node], CURVE_DISTANCE))


        # 直线边
        for i in range(left_id, right_id):
            node0 = quad_nodes[i]
            if node0.is_vertical():
                node1 = QuadNode([(node0.cells[0][0], node0.cells[0][1] - 1),
                                  (node0.cells[1][0], node0.cells[1][1] - 1),
                                  (node0.cells[2][0], node0.cells[2][1] - 1),
                                  (node0.cells[3][0], node0.cells[3][1] - 1)])
                if quad_map.get(node1):
                    quad_nodes[i].neighbor.append((quad_map[node1], STRAIGHT_DISTANCE))
                node1 = QuadNode([(node0.cells[0][0], node0.cells[0][1] + 1),
                                  (node0.cells[1][0], node0.cells[1][1] + 1),
                                  (node0.cells[2][0], node0.cells[2][1] + 1),
                                  (node0.cells[3][0], node0.cells[3][1] + 1)])
                if quad_map.get(node1):
                    quad_nodes[i].neighbor.append((quad_map[node1], STRAIGHT_DISTANCE))
            if node0.is_horizontal():
                node1 = QuadNode([(node0.cells[0][0] - 1, node0.cells[0][1]),
                                  (node0.cells[1][0] - 1, node0.cells[1][1]),
                                  (node0.cells[2][0] - 1, node0.cells[2][1]),
                                  (node0.cells[3][0] - 1, node0.cells[3][1])])
                if quad_map.get(node1):
                    quad_nodes[i].neighbor.append((quad_map[node1], STRAIGHT_DISTANCE))
                node1 = QuadNode([(node0.cells[0][0] + 1, node0.cells[0][1]),
                                  (node0.cells[1][0] + 1, node0.cells[1][1]),
                                  (node0.cells[2][0] + 1, node0.cells[2][1]),
                                  (node0.cells[3][0] + 1, node0.cells[3][1])])
                if quad_map.get(node1):
                    quad_nodes[i].neighbor.append((quad_map[node1], STRAIGHT_DISTANCE))

    # 多线程建边
    threads = []
    chuck = len(quad_nodes) // THREADS
    for i in range(THREADS):
        left = i * chuck
        right = (i + 1) * chuck if i != THREADS - 1 else len(quad_nodes)
        thread = threading.Thread(target=add_edge_task, args=(left, right))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    # 打乱边的顺序，让路径看起来更随机
    for i in range(len(quad_nodes)):
        random.shuffle(quad_nodes[i].neighbor)

    #保存到文件缓存
    QuadNode.save_to_file(quad_nodes, quad_map)

    return quad_map, quad_nodes


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
