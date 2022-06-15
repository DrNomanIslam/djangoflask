from django.contrib import admin
from django.urls import path, register_converter
from .views import attendance_new, auth, bar, daily, daily_employee, daily_today, department_new, employee_new, employees, font, get_time_sheet, index, logout_user, manage, payroll, validate_employee, weekly, weekly_current, login_user

urlpatterns = [
    path('', index, name='index'),
    path('employees', employees, name='employee_report'),
    path('employees/<str:action>/<str:emp_id>', employees, name='employee_report'),
    path('employee/new', employee_new, name='employee_new'),
    path('attendance/<str:emp_id>', attendance_new, name='attendance_new'),
    path('department/new', department_new, name='department_new'),
    path('daily', daily_today, name='daily_today'),
    path('payroll', payroll, name='payroll'),
    path('daily/<int:todo>/<str:dt>', daily, name='daily'),
    path('daily/<int:todo>/<str:dt>/<str:filter>/<str:value>', daily, name='daily filter'),
    path('weekly', weekly_current, name='weekly_current'),
    path('weekly/<int:todo>/<str:dt>', weekly, name='weekly'),
    path('timesheet/<int:emp_id>', get_time_sheet, name='timesheet'),
    path('timesheet/<int:emp_id>/<str:date>/<str:action>', get_time_sheet, name='timesheet'),
    path('bar/<int:emp_id>', bar, name='bar'),
    path('font', font, name='font'),
    path('manage', manage, name='font'),
    path('validate_emp_id', validate_employee, name='validate_employee'),
    path('login', login_user, name='login_page'),
    path('logout', logout_user, name='logout_page'),
    path('authenticate', auth, name='authenticate'),
]