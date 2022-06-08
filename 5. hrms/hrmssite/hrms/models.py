from django.db import models

# Create your models here.
from django.db import models

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, null=True)
    emp_name = models.CharField(max_length=20)
    dept = models.CharField(max_length=20)

class Attendance(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(max_length=20)
    time_in = models.DateTimeField(max_length=20)
    time_out = models.DateTimeField(max_length=20, null=True)
    hours = models.FloatField(default=0)