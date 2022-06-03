from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from . import weather_api
from .forms import WeatherForm

def index(request):
	if request.method == 'POST':
		form = WeatherForm(request.POST)
		if form.is_valid():
			city = form.cleaned_data['city']
			x = weather_api.get_weather(city)
			if x["cod"] != "404":
				y = x["main"]
				current_temperature = y["temp"] 
				current_pressure = y["pressure"] 
				current_humidity = y["humidity"] 
				z = x["weather"] 
				weather_description = z[0]["description"]
				return render(request,'weather.html',{'city':city,'error':'','temperature': current_temperature, 'pressure':current_pressure,'humidity':current_humidity, 'description':weather_description, 'form': form})
			else:
				return render(request,'weather.html',{'city':city, 'error': 'City not found', 'form': form})
	else:
		form = WeatherForm()
		return render(request,'weather.html',{'form': form})
    