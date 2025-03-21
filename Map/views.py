from django.shortcuts import render

from django.http import HttpResponse

from django.db import models

import DataSearch.service as data_service
import DataSearch.generate as gen

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from typing import Dict, Tuple, Union
import copy
import random

map0 = []
errJsonResponse = {
    '未找到可行路径': JsonResponse({
        'status': 'error',
        'message': '未找到可行路径'
    }, status=401),
    '内部错误':      JsonResponse({
       'status': 'error',
       'message': '内部错误'
    }, status=402),
    '仅支持POST请求': JsonResponse({
      'status': 'error',
      'message': '仅支持POST请求'
    }, status=403),
}

# Create your views here.
def index(request):
    global map0

    row, col = 100, 170
    map0 = [['empty' for _ in range(col)] for _ in range(row)]
    # gen.generate_map01(row, col)
    context = {
        "map0": map0,
    }

    # 车位
    all_ps = data_service.get_car_positions()
    for p in all_ps:
        for i in range(p.LU_x_coord, p.RD_x_coord + 1):
            for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                if p.is_occupied:
                    map0[i][j] = 'occupy'
                else:
                    map0[i][j] = 'free'

    # 障碍物
    for i in range(65, 75):
        for j in range(40, 50):
            map0[i][j] = 'border'
    for i in range(30, 40):
        for j in range(120, 130):
            map0[i][j] = 'border'

    # 入口
    for i in range(48, 53):
        map0[i][0] = 'entry'

    return render(request, "map.html", context)


@csrf_exempt
def parking_request(request):
    global map0, errJsonResponse
    map1 = copy.deepcopy(map0)  # 同样使用深拷贝

    if request.method == 'POST':
        try:
            target_x = int(request.POST.get('x'))
            target_y = int(request.POST.get('y'))

            nodes = []
           



            # 返回JSON格式响应
            return JsonResponse({
                'status': 'success',
                'map': map1,  # 更新后的地图数据
                'message': '停车操作成功'
            })
        except Exception as e: return errJsonResponse['内部错误']

    return errJsonResponse['仅支持POST请求']



# 在文件顶部添加导入

@csrf_exempt
def finding_request(request):
    global map0, errJsonResponse
    map1 = copy.deepcopy(map0)

    if request.method == 'POST':
        try:
            target_x = int(request.POST.get('x'))
            target_y = int(request.POST.get('y'))
            # 在路径搜索前处理目标停车位
            all_ps = data_service.get_car_positions()
            for p in all_ps:
                # 检查目标点是否在该停车位范围内
                if (p.LU_x_coord <= target_x <= p.RD_x_coord and
                    p.LU_y_coord <= target_y <= p.RD_y_coord):
                    # 将该停车位全部标记为free
                    for i in range(p.LU_x_coord, p.RD_x_coord + 1):
                        for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                            map1[i][j] = 'free'
                    break
            
            # BFS最短路径算法
            path = []
            queue = [(50, 0)]
            visited: Dict[Tuple[int, int], Union[Tuple[int, int], None]] = {(50, 0): None}
            found = False
            current = None  # 添加初始化

            directions = [(-1,0), (1,0), (0,-1), (0,1)]

            for x in range(100):
                for y in range(170):
                    if map1[x][y] != 'empty':
                        continue
                    for dx, dy in directions:
                        next_y = y + dy    
                        next_x = x + dx
                        # 检查边界和可通行性
                        if (0 <= next_x < 100 and 0 <= next_y < 170 and
                            map1[next_x][next_y] == 'occupy'):
                            map1[x][y] = 'close'


            while queue and not found:
                current = queue.pop(0)     
                # 到达目标点
                if current == (target_x, target_y):
                    found = True
                    break
                random.shuffle(directions)  # 每次请求随机打乱方向顺序
                for dx, dy in directions:
                    next_x = current[0] + dx
                    next_y = current[1] + dy    
                    # 检查边界和可通行性
                    if (0 <= next_x < 100 and 0 <= next_y < 170 and
                        (next_x, next_y) not in visited and
                        map1[next_x][next_y] in ('free', 'entry', 'empty')):
                        
                        visited[(next_x, next_y)] = current
                        queue.append((next_x, next_y))
                
            # 回溯路径
            if found:
                while current:  # 此时current已明确绑定
                    path.append(current)
                    current = visited[current]
            
            map2 = copy.deepcopy(map0)
            # 绘制路径
            if found:
                for x, y in path:
                    if map2[x][y] != 'entry':  # 保留入口原色
                        map2[x][y] = 'path'
            else:
                return errJsonResponse['未找到可行路径']

            
            return JsonResponse({
                'status': 'success',
                'map': map2,
                'message': '路径规划成功'
            })
            
        except Exception as e: return errJsonResponse['内部错误']

    return errJsonResponse['仅支持POST请求']


@csrf_exempt
def reset(request):
    global map0, errJsonResponse
    if request.method == 'POST':
        return JsonResponse({
            'status': 'success',
            'map': map0,  # 直接返回原始map0
            'message': '恢复操作成功'
        })
    return errJsonResponse['仅支持POST请求']


