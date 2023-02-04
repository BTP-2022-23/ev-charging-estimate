from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.HomePage, name='home'),
]