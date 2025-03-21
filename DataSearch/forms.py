from django import forms
from .models import CarPosition

class AddCarPositionForm(forms.ModelForm):
    class Meta:
        model = CarPosition
        fields = ['LU_x_coord', 'LU_y_coord', 'RD_x_coord', 'RD_y_coord', 'is_occupied', 'free_time']
        labels = {
            'LU_x_coord': '左上角 X 坐标',
            'LU_y_coord': '左上角 Y 坐标',
            'RD_x_coord': '右下角 X 坐标',
            'RD_y_coord': '右下角 Y 坐标',
            'is_occupied': '是否被占用',
            'free_time': '空闲时间',
        }

class DeleteCarPositionForm(forms.Form):
    pos_id = forms.IntegerField(label="停车位编号", required=True)