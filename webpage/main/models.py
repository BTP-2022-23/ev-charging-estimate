from django.db import models

# Create your models here.
class CoordinatesForm(models.Model):
  # fields of the model
  Latitude = models.CharField(max_length = 20, default="30.9688367")
  Longitude = models.CharField(max_length = 20, default="76.526088")
  Rush_factor_alpha = models.CharField(max_length = 20, default="0.2")
  Prebooking_category = models.CharField(max_length = 20, default="2")
  Priority_rating = models.CharField(max_length = 20, default="2")