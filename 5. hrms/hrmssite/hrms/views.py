from email import message
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Attendance

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
		attds = Attendance.objects.filter(emp_id=emp_id)
		return render(request, 'attendance.html', {'message':message, 'attendance': attds})
	else:
		return render(request, 'attendance.html', {'message': ''})
