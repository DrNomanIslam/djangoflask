from django.db import models
from datetime import datetime

class Author(models.Model):
    author_id = models.CharField(max_length=10,default="")
    first_name = models.CharField(max_length=10,default="")
    last_name = models.CharField(max_length=10,default="")
    email = models.EmailField(max_length=40,default="")
    highest_qualification = models.CharField(max_length=10,default="")
    
    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

class Publication(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=200,default="")
    journal = models.CharField(max_length=50)
    year_of_publication = models.IntegerField(default=datetime.today().year)
    volume = models.IntegerField(default=1)
    issue = models.IntegerField(default=1)
    pp = models.CharField(max_length=15)
