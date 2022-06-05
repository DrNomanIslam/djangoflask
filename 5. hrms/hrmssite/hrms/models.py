from django.db import models

# Create your models here.
from django.db import models

class Attendance(models.Model):
    @property
    def hours(self):
        if(self.time_out):
            diff = self.time_out-self.time_in
            return diff.total_seconds() / 3600
        else:
            return 0


    emp_id = models.CharField(max_length=20)
    date = models.DateTimeField(max_length=20)
    time_in = models.DateTimeField(max_length=20)
    time_out = models.DateTimeField(max_length=20, null=True)


