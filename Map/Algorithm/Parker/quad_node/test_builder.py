import os
import django
import unittest

# 初始化Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')  # 替换为实际项目设置路径
django.setup()

from Map.Algorithm.Parker.quad_node.builder import get_quad


class TestBuilder(unittest.TestCase):
    def test_get_quad_map_normal(self):
        print("TEST")
        quad_map, quad_nodes = get_quad()
        total = 0
        for node in quad_nodes:
            total += len(node.neighbor)
        print("total: ", total)
        print("count: ", len(quad_nodes))

        self.assertGreater(len(quad_map), 0)
        self.assertGreater(len(quad_nodes), 0)


if __name__ == '__main__':
    unittest.main()
