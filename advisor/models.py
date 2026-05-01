"""
Models for the Air Quality Health Advisor app.

The AirQualityRecord model mirrors the columns in the Pakistan
Air Quality CSV so that data can be seeded, queried, and fed
into the ML prediction pipeline without column mismatches.
"""

from django.db import models


class AirQualityRecord(models.Model):
    """Single air-quality observation with health impact data."""

    # ---------- Air Quality Metrics ----------
    pm10 = models.FloatField(verbose_name="PM10")
    pm2_5 = models.FloatField(verbose_name="PM2.5")
    carbon_monoxide = models.FloatField(verbose_name="Carbon Monoxide")
    nitrogen_dioxide = models.FloatField(verbose_name="Nitrogen Dioxide")
    sulphur_dioxide = models.FloatField(verbose_name="Sulphur Dioxide")
    ozone = models.FloatField(verbose_name="Ozone")
    dust = models.FloatField(verbose_name="Dust")

    # ---------- Weather Conditions ----------
    temperature = models.FloatField(verbose_name="Temperature")
    humidity = models.FloatField(verbose_name="Humidity")
    precipitation = models.FloatField(verbose_name="Precipitation")
    wind_speed = models.FloatField(verbose_name="Wind Speed")
    pressure = models.FloatField(verbose_name="Pressure")

    # ---------- Health Impact Target ----------
    aqi_category = models.CharField(
        max_length=100,
        verbose_name="AQI Category",
        default="Good",
    )

    # ---------- Metadata ----------
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Air Quality Record"
        verbose_name_plural = "Air Quality Records"

    def __str__(self):
        return f"Record #{self.pk} | PM2.5={self.pm2_5:.1f} | Category={self.aqi_category}"

    # Maps CSV header -> Django model field name
    CSV_FIELD_MAP = {
        "pm10": "pm10",
        "pm2_5": "pm2_5",
        "carbon_monoxide": "carbon_monoxide",
        "nitrogen_dioxide": "nitrogen_dioxide",
        "sulphur_dioxide": "sulphur_dioxide",
        "ozone": "ozone",
        "dust": "dust",
        "temperature": "temperature",
        "humidity": "humidity",
        "precipitation": "precipitation",
        "wind_speed": "wind_speed",
        "pressure": "pressure",
        "aqi_category": "aqi_category",
    }
