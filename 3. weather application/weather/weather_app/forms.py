from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)