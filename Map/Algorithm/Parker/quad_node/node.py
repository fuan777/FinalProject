import copy
import pickle

from pathlib import Path
from typing import List

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



