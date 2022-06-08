from email import message
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import os
from sqlalchemy import null
from .models import Attendance, Employee
from django.db import connection


# Create your views here.


def index(request):
	emp_list = Employee.objects.filter()
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
			emp_name = 'Welcome ' + e.emp_name
		except Employee.DoesNotExist:
			return render(request, 'attendance.html', {'message': 'No employee exists', 'emp_list':emp_list})

		message = ''
		try:
			a = Attendance.objects.get(emp_id = e, date=dt)
			a.time_out=today.replace(tzinfo=None)
			a.time_in = a.time_in.replace(tzinfo=None)
			diff = a.time_out-a.time_in
			a.hours = diff.total_seconds() / 3600
			print('The hours value is ' , a.hours)
			a.save()
			message = 'You have successfully timed out'
		except Attendance.DoesNotExist:
			a = Attendance(emp_id=e, date=dt)
			a.time_in = time
			a.save()
			message = 'You have successfully timed in'

		#getting all the attendance
		start, end = get_week_range(datetime.today())
		attds = Attendance.objects.filter(emp_id=e, date__gte=start, date__lte=end)
		total = get_total_hours(attds)
		return render(request, 'attendance.html', {'message':message, 'attendance': attds, 'total': total, 'emp_name': emp_name, 'emp_list':emp_list})
	else:
		return render(request, 'attendance.html', {'message': '', 'emp_list':emp_list})


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
		
		a = Attendance.objects.filter(date__gte=start, date__lte=end)
		start = start.strftime("%Y-%m-%d %H:%M")
		return render(request, 'weekly.html', {'message':message, 'attendance': a, 'dt': start})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for current week")

def payroll(request):
	dt = datetime.today()
	year, wk, day_of_week = dt.isocalendar()
	if(wk%2 == 0):
		dt = start + timedelta(days=-7)

	message = "Week Sarting - " + str(dt)
	pr = {}
	for i in range(2):
		start, end = get_week_range(dt)
		with connection.cursor() as cursor:
			cursor.execute("select emp_id_id, emp_name, sum(hours) as regular from hrms_Attendance, hrms_Employee where hrms_Employee.id=hrms_Attendance.emp_id_id and date>='"+str(start)+ "' and date<='" + str(end) +"' group by emp_id_id, emp_name")
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


def weekly_current(request):
	return weekly(request,0,None)

def bar(request,emp_id):
	return render(request,'bar.html', {'emp_id': emp_id})

def font(request):
	zip_file = open('free_3_of_9.zip', 'rb')
	response = HttpResponse(zip_file, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename="%s"' % 'font.zip'
	return response
	

def daily(request, todo ,dt):
	print('todo=',todo)
	if(todo == 0):
		today = datetime.now()
		dt = today.strftime("%Y-%m-%d")
		dt = dt + " 00:00"
	else:
		format = '%Y-%m-%d %H:%M'
		start = datetime.strptime(dt, format).date()
		if(todo==1):
			start = start + timedelta(days=1)
		else:
			start = start + timedelta(days=-1)

		dt = start.strftime("%Y-%m-%d")
		dt = dt + " 00:00"

	try:		
		
		a = Attendance.objects.filter(date=dt)
		print(dt)
		return render(request, 'daily.html', {'message':message, 'attendance': a, 'dt': dt})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for today")

def get_week_range(dt):
	start = dt - timedelta(days=dt.weekday())
	end = start + timedelta(days=6)
	return (start,end)

def get_time_sheet(request,emp_id):
	try:
		e = Employee.objects.get(emp_id=emp_id)
		emp_name = e.emp_name
		start, end = get_week_range(datetime.today())
		a = Attendance.objects.filter(emp_id=e,date__gte=start, date__lte=end)
		total = get_total_hours(a)
		return render(request, 'timesheet.html', {'attendance': a, 'emp_id':emp_id, 'emp_name': emp_name, 'total':total})
	except Employee.DoesNotExist:
		return HttpResponse("The employee doesn't exist")