from attr import attr
from django import forms
from sqlalchemy import null
from .models import Attendance, Department, Employee

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'time'

class EmployeeForm(forms.ModelForm):

    joining = forms.DateField(widget=DateInput)


    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = '__all__'

class AttendanceForm(forms.ModelForm):

    date = forms.DateField(widget=DateInput)
    #time_in = forms.DateField(widget=DateTimePickerInput)
    #time_out = forms.DateField(widget=DateTimePickerInput)

    hours = forms.FloatField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Attendance
        fields = '__all__'