# todo/todo/urls.py : Main urls.py
from django.contrib import admin
from django.urls import path, include
from .views import RestApiView,RestDetailApiView

urlpatterns = [
    path('api', RestApiView.as_view(), name='api'),
    path('api/<int:todo_id>/', RestDetailApiView.as_view()),
]