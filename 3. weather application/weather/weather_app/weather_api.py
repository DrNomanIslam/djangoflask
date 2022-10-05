import requests

api_key = "35896d0af3df12ebba30c41a66c13367"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city_name):
	complete_url = base_url + "appid=" + api_key + "&q=" + city_name
	response = requests.get(complete_url)
	return response.json()