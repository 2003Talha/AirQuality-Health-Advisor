from django import forms

from .models import AirQualityRecord


class AirQualityForm(forms.ModelForm):
    class Meta:
        model = AirQualityRecord
        # We only want users to input the features that the model uses for prediction.
        # Health impact score and class are predicted, not inputted.
        fields = [
            "aqi",
            "pm10",
            "pm2_5",
            "no2",
            "so2",
            "o3",
            "temperature",
            "humidity",
            "wind_speed",
            "respiratory_cases",
            "cardiovascular_cases",
            "hospital_admissions",
        ]
        widgets = {
            field: forms.NumberInput(attrs={"class": "form-control", "step": "any"})
            for field in fields
        }
