from email import message
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from .models import Attendance
from django.db.models import Sum

# Create your views here.


def index(request):
	if request.method == 'POST':
		emp_id = request.POST['emp_id']
		today = datetime.now()
		dt = today.strftime("%Y-%m-%d")
		dt = dt + " 00:00"
		time = today.strftime("%Y-%m-%d %H:%M")
		message = ''
		try:
			a = Attendance.objects.get(emp_id=emp_id, date=dt)
			a.time_out=time
			a.save()
			message = 'You have successfully timed out'
		except Attendance.DoesNotExist:
			a = Attendance(emp_id=emp_id, date=dt)
			a.time_in = time
			a.save()
			message = 'You have successfully timed in'

		#getting all the attendance
		start, end = get_current_week_range()
		attds = Attendance.objects.filter(emp_id=emp_id, date__gte=start, date__lte=end)
		total = 0
		for a in attds:
			total += a.hours
		return render(request, 'attendance.html', {'message':message, 'attendance': attds, 'total': total})
	else:
		return render(request, 'attendance.html', {'message': ''})


def weekly(request):
	try:
		start, end = get_current_week_range()
		a = Attendance.objects.filter(date__gte=start, date__lte=end)
		return render(request, 'weekly.html', {'message':message, 'attendance': a})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for current week")

def daily(request):
	try:		
		today = datetime.now()
		dt = today.strftime("%Y-%m-%d")
		dt = dt + " 00:00"
		a = Attendance.objects.filter(date=dt)
		return render(request, 'daily.html', {'message':message, 'attendance': a})
	except Attendance.DoesNotExist:
		return HttpResponse("No attendance for today")

def get_current_week_range():
	today = date.today()
	start = today - timedelta(days=today.weekday())
	end = start + timedelta(days=6)
	return (start,end)