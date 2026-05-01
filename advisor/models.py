"""
Models for the Air Quality Health Advisor app.

The AirQualityRecord model mirrors the columns in the Kaggle
air-quality CSV so that data can be seeded, queried, and fed
into the ML prediction pipeline without column mismatches.
"""

from django.db import models


class AirQualityRecord(models.Model):
    """Single air-quality observation with health impact data."""

    # ---------- Air Quality Metrics ----------
    aqi = models.FloatField(
        verbose_name="Air Quality Index (AQI)",
        help_text="Composite air quality index value.",
    )
    pm10 = models.FloatField(
        verbose_name="PM10",
        help_text="Particulate matter <= 10 micrometres (ug/m3).",
    )
    pm2_5 = models.FloatField(
        verbose_name="PM2.5",
        help_text="Particulate matter <= 2.5 micrometres (ug/m3).",
    )
    no2 = models.FloatField(
        verbose_name="NO2",
        help_text="Nitrogen dioxide concentration (ppb).",
    )
    so2 = models.FloatField(
        verbose_name="SO2",
        help_text="Sulphur dioxide concentration (ppb).",
    )
    o3 = models.FloatField(
        verbose_name="O3",
        help_text="Ground-level ozone concentration (ppb).",
    )

    # ---------- Weather Conditions ----------
    temperature = models.FloatField(
        verbose_name="Temperature",
        help_text="Ambient temperature (Celsius).",
    )
    humidity = models.FloatField(
        verbose_name="Humidity",
        help_text="Relative humidity (%).",
    )
    wind_speed = models.FloatField(
        verbose_name="Wind Speed",
        help_text="Wind speed (m/s).",
    )

    # ---------- Health Impact ----------
    respiratory_cases = models.IntegerField(
        verbose_name="Respiratory Cases",
        help_text="Number of respiratory cases reported.",
    )
    cardiovascular_cases = models.IntegerField(
        verbose_name="Cardiovascular Cases",
        help_text="Number of cardiovascular cases reported.",
    )
    hospital_admissions = models.IntegerField(
        verbose_name="Hospital Admissions",
        help_text="Number of hospital admissions.",
    )
    health_impact_score = models.FloatField(
        verbose_name="Health Impact Score",
        help_text="Composite health impact score (0-100).",
    )
    health_impact_class = models.IntegerField(
        verbose_name="Health Impact Class",
        help_text="Predicted class: 0=Good, 1=Moderate, 2=Unhealthy-Sensitive, 3=Unhealthy, 4=Hazardous.",
        choices=[
            (0, "Good - No health impact"),
            (1, "Moderate - Minor irritation possible"),
            (2, "Unhealthy for Sensitive Groups"),
            (3, "Unhealthy - Significant risk"),
            (4, "Hazardous - Emergency conditions"),
        ],
        default=0,
    )

    # ---------- Metadata ----------
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Air Quality Record"
        verbose_name_plural = "Air Quality Records"

    def __str__(self):
        return f"Record #{self.pk} | AQI={self.aqi:.1f} | Class={self.health_impact_class}"

    # ----- CSV column mapping (used by the seed script) -----
    # Maps CSV header -> Django model field name
    CSV_FIELD_MAP = {
        "AQI": "aqi",
        "PM10": "pm10",
        "PM2_5": "pm2_5",
        "NO2": "no2",
        "SO2": "so2",
        "O3": "o3",
        "Temperature": "temperature",
        "Humidity": "humidity",
        "WindSpeed": "wind_speed",
        "RespiratoryCases": "respiratory_cases",
        "CardiovascularCases": "cardiovascular_cases",
        "HospitalAdmissions": "hospital_admissions",
        "HealthImpactScore": "health_impact_score",
        "HealthImpactClass": "health_impact_class",
    }
