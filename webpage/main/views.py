from django.shortcuts import render

import numpy as np

from .forms import *

# for API handeling
import requests
import json
from datetime import datetime
from pytz import timezone
import timezonefinder

# for saving and loading model
from joblib import Parallel, delayed
import joblib
# import sklearn




# The below function handles the API call.
def API_handler(lat=30.9688367,lon=76.526088):

    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    dd = datetime.now(timezone(timezone_str))
    month = dd.month
    day = dd.day
    hour = dd.hour

    url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid=2865c640108f7ea2169c32049fb48227"
    response = requests.get(url)

    if response.status_code == 200:
        print("Sucessfully fetched the data from the API.")
        # print(response.json())
    else:
        print(f"Hello User!, there's a {response.status_code} error with your request. Can not fetch the data.")

    fetched_data = response.json()
    # print(json.dumps(fetched_data, indent = 3))

    temp = fetched_data['main']['temp']
    feels_like = fetched_data['main']['feels_like']
    pressure = fetched_data['main']['pressure']
    humidity = fetched_data['main']['humidity']
    wind_speed = fetched_data['wind']['speed']
    clouds = fetched_data['clouds']['all']

    return np.array([[month,day, hour, temp, feels_like, pressure, humidity, wind_speed, clouds]])

# Create your views here.
def HomePage(request):
  loaded_model = joblib.load('main/model/ropar_model.pkl')
  # res = loaded_model.predict(API_handler())
  lat = 30.9688367
  lon = 76.526088
  form = CoordinatesForm()
  if request.method == 'POST':
    try:
      lat = float(request.POST.get("Latitude"))
      lon = float(request.POST.get("Longitude"))
    except:
      pass
  
  res = loaded_model.predict(API_handler(lat,lon))

  return render(request,'main/home.html', {'res':res[0], 'form':form})