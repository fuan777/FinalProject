import os
import django
import pytest


# 初始化Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')  # 替换为实际项目设置路径
django.setup()

from Map.Algorithm.Parker.QuadNode import get_all_quad_nodes, QuadNode


# 测试正常情况
def test_get_quad_map_normal():
    quad_map, quad_nodes = get_all_quad_nodes()
    print("YES")
    total = 0
    for node in quad_nodes:
        total += len(node.neighbor)

    print("total!!!", total)
    print("count:!!!!", len(quad_nodes))


    assert len(quad_map) > 0
