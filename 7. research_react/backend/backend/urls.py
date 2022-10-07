from django.contrib import admin
from django.urls import path,include               
from rest_framework import routers                 
from backend import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.PublicationView.as_view()),
    path('api/author', views.AuthorView.as_view())
]