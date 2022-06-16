from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/year/<int:year>', views.year_wise, name='year_wise'),
    path('index/author/<str:author>', views.author_wise, name='author_wise'),
    path('add', views.add, name='add'),
    path('edit/<str:p_id>', views.edit, name='edit'),
    path('delete/<str:p_id>', views.delete, name='delete'),
    path('add_author', views.add_author, name='add_author'),
    path('search', views.search, name='search'),
]