from django.http import HttpResponse
from django.shortcuts import render, redirect
from DataSearch.models import CarPosition
from DataSearch.forms import AddCarPositionForm
from DataSearch.forms import DeleteCarPositionForm

def success(request):
    return render(request, 'success.html')
# Create your views here.
def add_car_position(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['is_occupied'] = '0'

        form = AddCarPositionForm(data)
        if form.is_valid():
            # 创建一个新的 CarPosition 实例并保存
            new_position = form.save(commit=False)
            new_position.car_pos_id = CarPosition.objects.count() + 1
            new_position.is_occupied = False
            new_position.save()
            print(new_position.car_pos_id)
            return redirect('success_url')  # 重定向到成功页面
        else:
            print(form.errors)
        return render(request, 'manager.html', {'form': form})
    return render(request, 'manager.html')

def del_car_position(request):
    if request.method == "POST":
        form = DeleteCarPositionForm(request.POST)
        if form.is_valid():
            pos_id = form.cleaned_data['pos_id']
            try:
                # 根据编号删除停车位记录
                CarPosition.objects.get(car_pos_id=pos_id).delete()
                return redirect('success_url')
            except CarPosition.DoesNotExist:
                form.add_error('pos_id', '停车位编号不存在！')
    else:
        form = DeleteCarPositionForm()

    return render(request, 'manager.html', {'form': form})