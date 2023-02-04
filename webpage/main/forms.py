from django import forms
from .models import CoordinatesForm
  
# create a ModelForm
class CoordinatesForm(forms.ModelForm):
    class Meta:
        model = CoordinatesForm
        fields = ["Latitude","Longitude"]
        widgets = {'Latitude': forms.TextInput(attrs={'value':'30.9688367'}), 'Longitude': forms.TextInput(attrs={'value':'76.526088'})}
