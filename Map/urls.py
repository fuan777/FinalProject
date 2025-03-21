from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('parking/', views.parking_request),
    path('finding/', views.finding_request),
    path('reset/', views.reset),
]