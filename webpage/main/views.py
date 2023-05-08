from django.shortcuts import render

from .forms import *

from main import model_util


# Create your views here.
def HomePage(request):
  # loaded_model = joblib.load('main/model/ropar_model.pkl')
  # res = loaded_model.predict(API_handler())
  lat = 30.9688367
  lon = 76.526088
  alpha = 0.2
  prebooking_category = 2
  priority_rating = 2
  form = CoordinatesForm()

  if request.method == 'POST':
    try:
      lat = float(request.POST.get("Latitude"))
      lon = float(request.POST.get("Longitude"))
      alpha = float(request.POST.get("Rush_factor_alpha"))
      prebooking_category = float(request.POST.get("Prebooking_category"))
      priority_rating = float(request.POST.get("Priority_rating"))
    except:
      pass
  
  s = f'latitude = {lat}\nlongitude = {lon}\nalpha = {alpha}\nprebooking_category = {prebooking_category}\npriority_rating = {priority_rating}\n'
  s += model_util.driver(lat, lon, alpha, prebooking_category, priority_rating)
  res = s.split('\n')
  return render(request,'main/home.html', {'res':res, 'form':form})