from django import forms
from .models import AirQualityRecord

class AirQualityForm(forms.ModelForm):
    """
    Form for adding a new Air Quality Record manually from the frontend.
    Excludes the generated/target fields so the user only inputs features.
    """
    class Meta:
        model = AirQualityRecord
        fields = [
            'pm10',
            'pm2_5',
            'carbon_monoxide',
            'nitrogen_dioxide',
            'sulphur_dioxide',
            'ozone',
            'dust',
            'temperature',
            'humidity',
            'precipitation',
            'wind_speed',
            'pressure',
        ]
        
        # Add bootstrap styling to all input fields
        widgets = {
            field: forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}) 
            for field in fields
        }
