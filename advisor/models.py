from django.db import models

class AirQualityRecord(models.Model):
    # Location Metadata
    city = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=100, default="Pakistan")

    # Environmental Metrics (Inputs for ML)
    pm10 = models.FloatField(verbose_name="PM10 (µg/m³)")
    pm2_5 = models.FloatField(verbose_name="PM2.5 (µg/m³)")
    carbon_monoxide = models.FloatField(verbose_name="Carbon Monoxide (µg/m³)")
    nitrogen_dioxide = models.FloatField(verbose_name="Nitrogen Dioxide (µg/m³)")
    sulphur_dioxide = models.FloatField(verbose_name="Sulphur Dioxide (µg/m³)")
    ozone = models.FloatField(verbose_name="Ozone (µg/m³)")
    dust = models.FloatField(verbose_name="Dust (µg/m³)")
    temperature = models.FloatField(verbose_name="Temperature (°C)")
    humidity = models.FloatField(verbose_name="Humidity (%)")
    precipitation = models.FloatField(verbose_name="Precipitation (mm)")
    wind_speed = models.FloatField(verbose_name="Wind Speed (m/s)")
    wind_direction = models.FloatField(null=True, blank=True, verbose_name="Wind Direction (°)")
    pressure = models.FloatField(verbose_name="Pressure (hPa)")

    # Time Metadata
    timestamp = models.DateTimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    hour = models.IntegerField(null=True, blank=True)
    day_of_week = models.CharField(max_length=20, null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    month_name = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    is_weekend = models.BooleanField(default=False)
    season = models.CharField(max_length=20, null=True, blank=True)

    # The Target/Result
    aqi_category = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} - {self.aqi_category} ({self.city})"

    CSV_FIELD_MAP = {
        'timestamp': 'timestamp',
        'city': 'city',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'pm10': 'pm10',
        'pm2_5': 'pm2_5',
        'carbon_monoxide': 'carbon_monoxide',
        'nitrogen_dioxide': 'nitrogen_dioxide',
        'sulphur_dioxide': 'sulphur_dioxide',
        'ozone': 'ozone',
        'dust': 'dust',
        'temperature': 'temperature',
        'humidity': 'humidity',
        'precipitation': 'precipitation',
        'wind_speed': 'wind_speed',
        'wind_direction': 'wind_direction',
        'pressure': 'pressure',
        'date': 'date',
        'hour': 'hour',
        'day_of_week': 'day_of_week',
        'month': 'month',
        'month_name': 'month_name',
        'year': 'year',
        'is_weekend': 'is_weekend',
        'season': 'season',
        'aqi_category': 'aqi_category'
    }
