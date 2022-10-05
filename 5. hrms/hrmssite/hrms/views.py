from email import message
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import os
from sqlalchemy import null

from hrms.forms import EmployeeForm, DepartmentForm, AttendanceForm
from .models import Attendance, Department, Employee
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):	
	if request.method == 'POST':
		emp_id = request.POST['emp_id']
		today = datetime.now()
		dt = today.strftime("%Y-%m-%d")
		dt = dt + " 00:00"
		time = today.strftime("%Y-%m-%d %H:%M")
		emp_name = ''
		e = None
		try:
			e = Employee.objects.get(emp_id=emp_id)
			emp_name = e.emp_name
		except Employee.DoesNotExist:
			return render(request, 'attendance.html', {'message': 'No employee exists'})

		message = ''
		try:
			a = Attendance.objects.get(employee = e, date=dt)
			a.time_out=today.replace(tzinfo=None)
			a.time_in = a.time_in.replace(tzinfo=None)
			diff = a.time_out-a.time_in
			a.hours = diff.total_seconds() / 3600
			print('The hours value is ' , a.hours)
			a.save()
			message = 'Good bye ' + emp_name + '. You have successfully timed out'
		except Attendance.DoesNotExist:
			a = Attendance(employee=e, date=dt)
			a.time_in = time
			a.save()
			message = 'Welcome ' + emp_name + '. You have successfully timed In'

		#getting all the attendance
		start, end = get_week_range(datetime.today())
		attds = Attendance.objects.filter(employee=e, date__gte=start, date__lte=end)
		total = get_total_hours(attds)
		return render(request, 'attendance.html', {'message':message, 'attendance': attds, 'total': total, 'emp_name': emp_name})
	else:
		return render(request, 'attendance.html', {'message': ''})


def get_total_hours(attds):
	total = 0
	for a in attds:
		total += a.hours
	return total


def weekly(request,todo,dt):
	start, end = 0, 0
	if(todo==0):
		start, end = get_week_range(datetime.today())

	else:
		format = '%Y-%m-%d %H:%M'
		start = datetime.strptime(dt, format).date()
		if todo==1:
			start = start + timedelta(days=7)
		else:
			start = start + timedelta(days=-7)

		start, end = get_week_range(start)

	try:
		
		a = Attendance.objects.filter(date__gte=start, date__lte=end).all()

		start = start.strftime("%Y-%m-%d %H:%M")
		return render(request, 'weekly.html', {'message':message, 'attendance': a, 'dt': start})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for current week")

def payroll(request):
	dt = datetime.today()
	year, wk, day_of_week = dt.isocalendar()
	if(wk%2 == 0):
		dt = dt + timedelta(days=-7)

	message = "Week Sarting - " + str(dt)
	pr = {}
	for i in range(2):
		start, end = get_week_range(dt)
		with connection.cursor() as cursor:
			cursor.execute("select emp_id, emp_name, sum(hours) as regular from hrms_Attendance, hrms_Employee where hrms_Employee.emp_id=hrms_Attendance.employee_id and date>='"+str(start)+ "' and date<='" + str(end) +"' group by Employee_id, emp_name")
			rows = cursor.fetchall()

			for r in rows:
				overtime = 0
				if(int(r[2])>40):
					overtime = float(r[2]) - 40
				else:
					overtime = 0

				if(i==0):
					pr[r[0]] = [r[1],r[2], overtime, float(r[2]) + overtime, 0,0,0]
				else:
					try:
						pr[r[0]][4:] = [r[1],overtime, float(r[1]) + overtime]
					except:
						pr[r[0]] = [r[1],0,0,0,r[2], overtime, float(r[2]) + overtime]

		dt = dt + timedelta(days=7)

	return render(request,'payroll.html',{'pr':pr, 'message': message})

def daily_today(request):
	today = datetime.now()
	dt = today.strftime("%Y-%m-%d")
	dt = dt + " 00:00"
	return daily(request,0,dt)


def daily_employee(request, emp_id):
	today = datetime.now()
	dt = today.strftime("%Y-%m-%d")
	dt = dt + " 00:00"
	return daily(request,0,dt)


def weekly_current(request):
	return weekly(request,0,None)

def bar(request,emp_id):
	return render(request,'bar.html', {'emp_id': emp_id})

def font(request):
	zip_file = open('free_3_of_9.zip', 'rb')
	response = HttpResponse(zip_file, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename="%s"' % 'font.zip'
	return response



def daily(request, todo ,dt,filter=None, value=None):
	print('dt=',dt)
	if(todo == 0):
		today = datetime.strptime(dt, "%Y-%m-%d %H:%M")
		dt = today.strftime("%Y-%m-%d")
		dt = dt + " 00:00"
	else:
		format = '%Y-%m-%d %H:%M'
		start = datetime.strptime(dt, format).date()
		if(todo==1):
			start = start + timedelta(days=1)
		elif(todo==2):
			start = start + timedelta(days=-1)

		dt = start.strftime("%Y-%m-%d")
		dt = dt + " 00:00"

	try:	
		a = None
		
		if(filter == 'emp_id'):
			e = Employee.objects.get(emp_id=value)
			a = Attendance.objects.filter(date=dt,employee= e).all()
		elif(filter == 'dept_id'):
			d = Department.objects.get(dept_id=value)
			e = Employee.objects.get(department= d)
			a = Attendance.objects.filter(date=dt,employee=e).all()
		else:
			a = Attendance.objects.filter(date=dt).all()

		return render(request, 'daily.html', {'message':message, 'attendance': a, 'dt': dt, 'filter': filter, 'value': value})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for today")

def get_week_range(dt):
	start = dt - timedelta(days=dt.weekday())
	end = start + timedelta(days=6)
	return (start,end)

def get_time_sheet(request,emp_id, date=None, action=None):
	msg = ''
	if(action == 'edit'):
		e = Employee.objects.get(pk=emp_id)
		print(e)
		a = Attendance.objects.filter(employee=e,date=date).first()
		print(a)
		frm = AttendanceForm(instance=a)
		return render(request, 'new_attendance.html', {'form':frm, 'emp_id': emp_id})

	elif(action=='delete'):
		try:
			e = Employee.objects.get(pk=emp_id)
			print(e)
			print(date)
			a = Attendance.objects.get(employee=e,date=date)
			a.delete()
			msg = 'The attendance has been deleted successfully'
		except Attendance.DoesNotExist:
			msg = "The attendance doesn't exist"


	e = Employee.objects.get(emp_id=emp_id)
	emp_name = e.emp_name
#	start, end = get_week_range(datetime.today())
	a = Attendance.objects.filter(employee=e)
	total = get_total_hours(a)
	return render(request, 'timesheet.html', {'attendance': a, 'emp_id':emp_id, 'emp_name': emp_name, 'total':total, 'message': msg})

@login_required(login_url='/hrms/login')
def manage(request):
	emp_list = Employee.objects.filter()
	return render(request,'manage.html', {'emp_list': emp_list})


def employees(request,action=None,emp_id=None):
	msg = ''
	if(action=='delete'):
		try:
			e = Employee.objects.get(pk=emp_id)
			e.delete()
			msg = 'The employee has been deleted successfully'
		except Employee.DoesNotExist:
			msg = "The employee doesn't exist"

	elif(action=='edit'):
		p = Employee.objects.get(pk=emp_id)
		frm = EmployeeForm(instance=p)
		return render(request, 'new_employee.html', {'form':frm, 'joining': frm['joining']})

	emps = Employee.objects.all()
	return render(request,'employees.html', {'employees': emps, 'message': msg})

def employee_new(request):
	if request.method == 'GET':
		form = EmployeeForm()		
		return render(request,'new_employee.html', {'form': form})
	else:
		emp_id = request.POST['emp_id']
		instance = get_object_or_404(Employee, emp_id=emp_id)
		form = EmployeeForm(request.POST or None, instance=instance)
		#form.fields['emp_id'].disabled = True	
		if(form.is_valid()):
			form.save()
			return render(request,'new_employee.html', {'form': form, 'message': 'Employee has been saved'})
		else:			
			return render(request,'new_employee.html', {'form': form})


def attendance_new(request, emp_id=None):
	if request.method == 'GET':
		form = AttendanceForm()		
		form.fields['employee'].initial = emp_id
		return render(request,'new_attendance.html', {'form': form, 'emp_id': emp_id})
	else:
		emp_id = request.POST['employee']
		date = request.POST['date']
		
		d = request.POST.copy()
		
		time_in = ''
		time_out = ''
		try:
			format = '%Y-%m-%d %H:%M:%S'
			time_in = datetime.strptime(request.POST['time_in'], format)
			time_out = datetime.strptime(request.POST['time_out'], format)
		except:
			format = '%Y-%m-%d %H:%M:%S'
			time_in = date + ' ' + request.POST['time_in']
			time_out = date + ' ' + request.POST['time_out']
			time_in = datetime.strptime(time_in, format)
			time_out = datetime.strptime(time_out, format)
		
		diff = time_out-time_in
		hours = diff.total_seconds() / 3600


		d['time_in'] = time_in
		d['time_out'] = time_out

		d['hours'] = hours

		e = Employee.objects.get(pk=emp_id)
		a = Attendance.objects.filter(employee = e , date = date).first()
		
		form = AttendanceForm(d or None, instance=a)
		
		if(form.is_valid()):		
#			form.fields['employee'].disabled = True
#			form.fields['date'].disabled = True
			form.save()
			return render(request,'new_attendance.html', {'form': form, 'message': 'Attendance has been saved', 'emp_id': emp_id})
		else:			
			return render(request,'new_attendance.html', {'form': form, 'message': 'There are some problems in saving data','emp_id': emp_id})

def department_new(request):
	if request.method == 'GET':
		form = DepartmentForm()
		return render(request,'new_department.html', {'form': form})
	else:
		form = DepartmentForm(request.POST)
		if(form.is_valid()):
			form.save()
			return render(request,'new_department.html', {'form': form, 'message': 'Department has been saved'})
		else:			
			return render(request,'new_department.html', {'form': form})

def validate_employee(request):
	emp_id = request.GET.get('emp_id', None)
	data = {
		'is_taken': Employee.objects.filter(emp_id__iexact=emp_id).exists()
    }
	return JsonResponse(data)

def auth(request):
	id = request.GET.get('id', None)
	pwd = request.GET.get('pwd', None)
	user = authenticate(request, username=id, password=pwd)
	if user is not None:
		login(request, user)		
	data = {
		'auth': user is not None
    }
	
	return JsonResponse(data)	

def login_user(request):
	return render(request,'login.html')

def logout_user(request):
	logout(request)
	return render(request,'login.html')