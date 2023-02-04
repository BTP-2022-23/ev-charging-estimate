from django.db import models

# Create your models here.
class CoordinatesForm(models.Model):
  # fields of the model
  Latitude = models.CharField(max_length = 20, default="30.9688367")
  Longitude = models.CharField(max_length = 20, default="76.526088")