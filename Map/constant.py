from django.http import JsonResponse

MAP_ROWS = 100
MAP_COLS = 170

TEST_MAP_ROWS = 100
TEST_MAP_COLS = 170

ERR_JSON_RESPONSE = {
    '未找到可行路径': JsonResponse({'status': 'error', 'message': '未找到可行路径'}, status=401),
    '内部错误': JsonResponse({'status': 'error', 'message': '内部错误'}, status=500),
    '仅支持POST请求': JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=403)
}

DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]

DIA_DIRECTIONS = [(-1,-1), (-1,1), (1,-1), (1,1)]

THREADS = 8


#直线距离定义
STRAIGHT_DISTANCE = 3
#弯道距离定义
CURVE_DISTANCE = 1