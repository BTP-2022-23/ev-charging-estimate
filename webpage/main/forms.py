from django import forms
from .models import CoordinatesForm
  
# create a ModelForm
class CoordinatesForm(forms.ModelForm):
    class Meta:
        model = CoordinatesForm
        fields = ['Latitude','Longitude','Rush_factor_alpha','Prebooking_category','Priority_rating']
        widgets = {'Latitude': forms.TextInput(attrs={'value':'30.9688367'}),
                    'Longitude': forms.TextInput(attrs={'value':'76.526088'}),
                    'Rush_factor_alpha': forms.TextInput(attrs={'value':'0.2'}),
                    'Prebooking_category': forms.TextInput(attrs={'value':'2'}),
                    'Priority_rating': forms.TextInput(attrs={'value':'2'})}

