import copy
import os

import django

# 初始化Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')  # 替换为实际项目设置路径
django.setup()

from Map.Algorithm.Parker.QuadNode import get_quad, QuadNode

from constant import *


# 测试顺便生成缓存
def test_get_quad_map_normal():
    quad_map, quad_nodes = get_quad()
    print("YES")
    total = 0
    for node in quad_nodes:
        total += len(node.neighbor)

    # n = QuadNode([(25, 76), (26, 76), (27, 76), (27, 77)], 1)
    # print(quad_nodes[quad_map[n]].neighbor)
    # print(quad_nodes[quad_map[n]].get_space())
    #
    # print(quad_nodes[117064].cells, quad_nodes[117064].dir)
    # print(quad_nodes[121749].cells, quad_nodes[121749].dir)
    # print(quad_nodes[121749].get_space())


    n1 = QuadNode([(48, 0), (49, 0), (50, 0), (51, 0)], 1)
    n2 = QuadNode([(49, 1), (49, 0), (50, 0), (51, 0)], 1)



    print(n1.is_curve_close(n2))
    # print(quad_map.get(n2))
    print(quad_nodes[quad_map[n1]].neighbor)
    # print(quad_nodes[223446].cells, quad_nodes[223446].dir)
    print("total!!!", total)
    print("count:!!!!", len(quad_nodes))

    assert len(quad_map) > 0
