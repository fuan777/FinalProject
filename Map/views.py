from django.shortcuts import render

from django.http import HttpResponse

from django.db import models

import DataSearch.service as data_service
import DataSearch.generate as gen


# Create your views here.
def index(request):
    row, col = 100, 170

    gen.generate_map01(row, col)
    #     ['empty', '#FFFAF0'],
    #     ['border', '#000000'],
    #     ['path', '#d71345'],
    #     ['free', '#007d65'],
    #     ['occupy', '#102b6a'],
    map0 = [['empty' for _ in range(col)] for _ in range(row)]
    context = {
        "map0": map0,
    }
    all_ps = data_service.get_car_positions()
    for p in all_ps:
        for i in range(p.LU_x_coord, p.RD_x_coord + 1):
            for j in range(p.LU_y_coord, p.RD_y_coord + 1):
                if p.is_occupied:
                    map0[i][j] = 'occupy'
                else:
                    map0[i][j] = 'free'

    for i in range(65, 75):
        for j in range(40, 50):
            map0[i][j] = 'border'
    for i in range(30, 40):
        for j in range(120, 130):
            map0[i][j] = 'border'

    return render(request, "map.html", context)


