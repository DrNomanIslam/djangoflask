from django.contrib import admin
from django.urls import path, register_converter
from .views import bar, daily, daily_today, font, get_time_sheet, index, payroll, weekly, weekly_current

urlpatterns = [
    path('', index, name='index'),
    path('daily', daily_today, name='daily_today'),
    path('payroll', payroll, name='payroll'),
    path('daily/<int:todo>/<str:dt>', daily, name='daily'),
    path('weekly', weekly_current, name='weekly_current'),
    path('weekly/<int:todo>/<str:dt>', weekly, name='weekly'),
    path('employee/<int:emp_id>', get_time_sheet, name='timesheet'),
    path('bar/<int:emp_id>', bar, name='bar'),
    path('font', font, name='font'),
]