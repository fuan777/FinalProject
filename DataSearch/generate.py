import random
from .models import CarPosition



def generate_map01(row=100, col=170):
    """生成3x7尺寸且不重叠的停车位地图"""
    CarPosition.objects.all().delete()

    positions = []

    generate_row(positions, 10, 10, 5, 2, spot_size=(4, 7))
    generate_row(positions, 10, 70, 10, 2, spot_size=(7, 4))
    generate_col(positions, 20, 10, 4, 3, spot_size=(4, 7))
    generate_col(positions, 60, 10, 3, 3, spot_size=(4, 7))

    generate_row(positions, 30, 30, 5, 2, spot_size=(4, 7))
    generate_row(positions, 40, 30, 5, 2, spot_size=(4, 7))
    generate_row(positions, 50, 30, 5, 2, spot_size=(4, 7))

    generate_col(positions, 60, 30, 4, 2, spot_size=(7, 4))
    generate_row(positions, 81, 37, 2, 2, spot_size=(4, 7))

    generate_col(positions, 19, 100, 4, 2, spot_size=(7, 4))

    generate_row(positions, 55, 90, 5, 2, spot_size=(4, 7))
    generate_row(positions, 65, 90, 5, 2, spot_size=(4, 7))
    generate_row(positions, 75, 90, 5, 2, spot_size=(4, 7))

    generate_row(positions, 30, 133, 3, 2, spot_size=(7, 4))
    generate_col(positions, 39, 145, 4, 2, spot_size=(7, 4))

    generate_col(positions, 56, 66, 4, 2, spot_size=(7, 4))


    # 创建数据库记录
    for pos_id, pos in enumerate(positions):
        is_occupied = random.random() < 0.8
        CarPosition.objects.create(
            car_pos_id=pos_id,
            LU_x_coord=pos['LU_x'],
            LU_y_coord=pos['LU_y'],
            RD_x_coord=pos['RD_x'],
            RD_y_coord=pos['RD_y'],
            is_occupied=is_occupied,
        )

    return positions


def generate_row(positions, start_x, start_y, num_spots, h_gap=1, spot_size=(3, 7)):
    """横向生成多个车位
    Args:
        positions: 存储车位的列表
        start_x: 起始行坐标
        start_y: 起始列坐标
        num_spots: 生成数量
        h_gap: 横向间隔
        spot_size: 车位尺寸 (height, width)
    """
    current_y = start_y

    for _ in range(num_spots):
        # 计算车位坐标
        rd_x = start_x + spot_size[0] - 1
        rd_y = current_y + spot_size[1] - 1

        # 添加车位
        positions.append({
            'LU_x': start_x,
            'LU_y': current_y,
            'RD_x': rd_x,
            'RD_y': rd_y
        })

        # 更新下一个车位的起始列坐标
        current_y = rd_y + h_gap + 1  # +1保证最小间隔

        # 超出列边界则停止生成
        if rd_y + h_gap >= 170:
            break

def generate_col(positions, start_x, start_y, num_spots, h_gap=1, spot_size=(3, 7)):
    """纵向生成多个车位
    Args:
        positions: 存储车位的列表
        start_x: 起始行坐标
        start_y: 起始列坐标
        num_spots: 生成数量
        h_gap: 横向间隔
        spot_size: 车位尺寸 (height, width)
    """
    current_x = start_x

    for _ in range(num_spots):
        # 计算车位坐标
        rd_x = current_x + spot_size[0] - 1
        rd_y = start_y + spot_size[1] - 1

        if rd_x >= 100 or rd_y >= 170:
            break

        # 添加车位
        positions.append({
            'LU_x': current_x,
            'LU_y': start_y,
            'RD_x': rd_x,
            'RD_y': rd_y
        })

        # 更新下一个车位的起始列坐标
        current_x = rd_x + h_gap + 1  # +1保证最小间隔

