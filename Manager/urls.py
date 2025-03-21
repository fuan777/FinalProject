from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.add_car_position, name="add_car_position"),
    path("del/", views.del_car_position, name="del_car_position"),
    path('success/', views.success, name='success_url'),
]