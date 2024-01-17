import requests
from django.shortcuts import render
import logging
import time

# Configure the logging settings
logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

# Create your views here.
def index(request):
    API_KEY = open("API_KEY.txt", "r").read()

    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    # if user fills out and submits form
    if request.method == "POST":

        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        if not city1:
            error_message = "You must fill at least City 1. Please check your input and try again."
            logging.error(error_message)
            context = {
                "error_message": error_message,
            }
            return render(request, "weather_app/index.html", context)

        # calls the fetch_weather function and inputs 3 arguments
        weather_data1 = fetch_weather(city1, API_KEY, current_weather_url)
        if city2:
            weather_data2 = fetch_weather(city2, API_KEY, current_weather_url)
        else:
            weather_data2 = None
        if weather_data1 is None or (city2 and weather_data2 is None): # if there is no weather_data1 or if there is city2 but the weather_data cannot be retrieved then there is an error but if there is simply no city2 then there is no error as user can input only one city if they want
            error_message = "Weather data couldn't be retrieved for the specified city names. Please check your input and try again. If this issue persists please email weatherappissues@gmail.com with your problem" #consider updating this so that users only have the option to email after 3 consecutive errors
            logging.error(error_message)
            context = {
                "error_message": error_message,
            }
            return render(request, "weather_app/index.html", context)
        else:   
            context = {
            "weather_data1": weather_data1,
            "weather_data2": weather_data2,
           }
            return render(request, "weather_app/index.html", context)
    # this else block is handling the case when the user accesses the page initially (e.g., by navigating to the URL) or when 
    # they submit a GET request or other non-POST requests. It renders and returns the "index.html" template, which is the 
    # initial page of the weather application. This allows users to view the page and submit a city name to fetch 
    # weather data via a POST request.
    else:
        return render(request, "weather_app/index.html")


def fetch_weather(city, api_key, current_weather_url):


    try: #try block contains code which may raise an exception/error when attempting to execute the request (sending a request to the OpenWeatherMap API to fetch weather data for a specific city)
         response = requests.get(current_weather_url.format(city, api_key)).json()
         if response['cod'] == 200:
             weather_data = {
                 "city": city,
                 "temperature": round(response['main']['temp'] - 273.15, 2),
                 "description": response['weather'][0]['description'],
                 "icon": response['weather'][0]['icon']
            }
             return weather_data
         else:
             logging.error("Error in retrieving weather data for city: %s", city)
             return None
    # except starts the exception handling block and the rest specifies the the type of exceptions being caught
    # requests.exceptions.RequestException - contains most exceptions that requests is likely to raise
    # storing the exception/error as e allows us to see what type of exception/error we have
    except requests.exceptions.RequestException as e:
        logging.error("Error in making request to OpenWeatherMap API: %s", e)
        return None
             


