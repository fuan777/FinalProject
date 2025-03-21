from .models import CarPosition

def get_car_positions():
    """获取所有停车位数据"""
    return CarPosition.objects.all()

def get_occupied_positions():
    """获取被占用的停车位"""
    return CarPosition.objects.filter(is_occupied=True)

def get_position_by_id(position_id):
    """通过ID获取停车位"""
    try:
        return CarPosition.objects.get(car_pos_id=position_id)
    except CarPosition.DoesNotExist:
        return None