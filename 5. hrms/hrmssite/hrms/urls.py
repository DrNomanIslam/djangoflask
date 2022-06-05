from django.contrib import admin
from django.urls import path
from .views import daily, index, weekly

urlpatterns = [
    path('', index, name='index'),
    path('daily', daily, name='daily'),
    path('weekly', weekly, name='weekly'),
]