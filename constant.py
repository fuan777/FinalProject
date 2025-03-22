from django.http import JsonResponse

# json err
ERR_JSON_RESPONSE = {
    '未找到可行路径': JsonResponse({'status': 'error', 'message': '未找到可行路径'}, status=401),
    '内部错误': JsonResponse({'status': 'error', 'message': '内部错误'}, status=500),
    '仅支持POST请求': JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=403)
}

# map size
MAP_ROWS = 100
MAP_COLS = 170

TEST_MAP_ROWS = 100
TEST_MAP_COLS = 170


# 方向
DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]

DIA_DIRECTIONS = [(-1,-1), (-1,1), (1,-1), (1,1)]


# 线程个数
THREADS = 8


# 直线距离定义
STRAIGHT_DISTANCE = 8
# 弯道距离定义
CURVE_DISTANCE = 3
# 距离无穷大定义
INF_DISTANCE = 1000000000


# 生成occupy占比
OCCUPY_RATIO = 1

# 常量是否需要更新
CONST_NEED_UPDATE = False