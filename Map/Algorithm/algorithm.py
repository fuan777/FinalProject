import heapq
import random
from typing import List, Tuple, Union, Dict

from Map.Algorithm.Parker.quad_node import QuadNode

from constant import *


# 单格点 bfs
# 单start，多end中取最短
def bfs(map0, start, end) -> Union[List[Tuple[int, int]], None]:
    path: List[Tuple[int, int]] = []
    queue = [start]
    last: Dict[Tuple[int, int], Union[Tuple[int, int], None]] = {start: None}
    current: Union[Tuple[int, int], None] = None
    end_set = set(end)
    found = False

    while queue and not found:
        current = queue.pop(0)

        if current in end_set:
            found = True
            break
        for dx, dy in RANDOM_DIRECTIONS[random.randint(0, 23)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            # 检查边界和可通行性
            if (0 <= next_x < MAP_ROWS and 0 <= next_y < MAP_COLS and
                    (next_x, next_y) not in last and
                    map0[next_x][next_y] in ('free', 'entry', 'empty')):
                last[(next_x, next_y)] = current
                queue.append((next_x, next_y))

    if found:
        while current:
            path.append(current)
            current = last[current]
        path.reverse()
        return path

    return None


# 四格点带权 dijkstra
# 单start，多end中最短路
def dijkstra(quad_nodes, map0, start, end) -> Union[List[QuadNode], None]:
    path : List[QuadNode] = []
    queue = [(0, start)]
    heapq.heapify(queue)

    visited = set()
    end_set = set(end)

    last : Dict[int, Union[int, None]] = {start: None}
    found = False
    current : Union[int, None] = None

    distance = [INF_DISTANCE for i in range(len(quad_nodes))]
    distance[start] = 0

    while queue and not found:
        dist, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)

        if current in end_set:
            found = True
            break
        for neighbor, weight in quad_nodes[current].neighbor:
            if (dist + weight < distance[neighbor] and
                    quad_nodes[neighbor].is_valid and neighbor not in visited):
                heapq.heappush(queue, (dist + weight, neighbor))
                distance[neighbor] = dist + weight
                last[neighbor] = current

    if found:
        while current:
            path.append(quad_nodes[current])
            current = last[current]
        path.reverse()
        return path

    return None