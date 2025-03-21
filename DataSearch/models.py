from django.db import models

# Create your models here.

class CarPosition(models.Model):
    car_pos_id = models.IntegerField(primary_key=True)
    LU_x_coord = models.IntegerField()
    LU_y_coord = models.IntegerField()
    RD_x_coord = models.IntegerField()
    RD_y_coord = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    free_time = models.IntegerField(default=None, null=True, blank=True)


class Pixel(models.Model):
    coord = models.IntegerField() #(x / 100, x % 170)
    status = models.CharField(max_length=20)

class Person(models.Model):
    person_name = models.CharField(primary_key=True, max_length=20)
    is_parking = models.BooleanField(default=False)
    car_pos_id = models.IntegerField(default=None, null=True)