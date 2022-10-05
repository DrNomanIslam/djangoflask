from django.db import models

# Create your models here.
from django.db import models


class Department(models.Model):
    dept_id = models.CharField(max_length=20, primary_key=True)
    dept_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.dept_name

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, primary_key=True)
    emp_name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), null=True, default='M')
    joining = models.DateField(null=True)

    def __str__(self) -> str:
        return self.emp_name



class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(max_length=20)
    time_in = models.DateTimeField(max_length=20)
    time_out = models.DateTimeField(max_length=20, null=True)
    hours = models.FloatField(default=0, null=True)