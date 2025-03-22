from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import copy

from Map.Algorithm.Parker.QuadNode import QuadNode

from Map.Algorithm.Finder.Finder import Finder
from Map.Algorithm.Parker.Parker import Parker
from Map.Algorithm.Gener import Gener
from Map.constant import *

'''全局唯一map地图'''
map0 = []

def index(request):
    global map0
    map0 = [['empty' for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]
    gener = Gener(map0)
    # 随机地图加入数据库
    # gener.gen_random()
    # 车位
    gener.set_car_pos()
    # 障碍物
    gener.set_border(65, 75, 40, 50)
    gener.set_border(30, 40, 120, 130)
    # 入口
    gener.set_entry(48, 52, 0, 1)

    return render(request, "map.html", {"map0": map0})

@csrf_exempt
def parking_request(request):
    global map0
    map2 = copy.deepcopy(map0)

    if request.method == 'POST':
        try:
            parker = Parker(map0, [(48, 0), (49, 0), (50, 0), (51, 0)], (int(request.POST.get('x')), int(request.POST.get('y'))))
            path = parker.find_path()
            if path:
                for node in path:
                    for x, y in node.cells:
                        if map2[x][y] != 'entry':
                            map2[x][y] = 'path'
            else:
                return ERR_JSON_RESPONSE['未找到可行路径']

            return JsonResponse({
                'status': 'success',
                'map': map2,
                'message': '路径规划成功'
            })
        except Exception as e:
            return ERR_JSON_RESPONSE['内部错误']

    return ERR_JSON_RESPONSE['仅支持POST请求']



@csrf_exempt
def finding_request(request):
    global map0
    map2 = copy.deepcopy(map0)

    if request.method == 'POST':
        try:
            finder = Finder(map0, (50, 0), (int(request.POST.get('x')),int(request.POST.get('y'))))
            path = finder.find_path()
            if path:
                for x, y in path:
                    if map2[x][y] != 'entry' and finder.inside(x, y) != True:
                        map2[x][y] = 'path'
            else:
                return ERR_JSON_RESPONSE['未找到可行路径']

            return JsonResponse({
                'status': 'success',
                'map': map2,
                'message': '路径规划成功'
            })
        except Exception as e: return ERR_JSON_RESPONSE['内部错误']

    return ERR_JSON_RESPONSE['仅支持POST请求']


@csrf_exempt
def reset(request):
    global map0
    if request.method == 'POST':
        return JsonResponse({
            'status': 'success',
            'map': map0,  # 直接返回原始map0
            'message': '恢复操作成功'
        })
    return ERR_JSON_RESPONSE['仅支持POST请求']


