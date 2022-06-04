from django.db import models

# Create your models here.
from django.db import models

class Attendance(models.Model):
    emp_id = models.CharField(max_length=20)
    date = models.DateTimeField(max_length=20)
    time_in = models.DateTimeField(max_length=20)
    time_out = models.DateTimeField(max_length=20, null=True)

