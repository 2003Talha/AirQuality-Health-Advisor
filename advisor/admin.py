from django.contrib import admin

from .models import AirQualityRecord


@admin.register(AirQualityRecord)
class AirQualityRecordAdmin(admin.ModelAdmin):
    """Admin interface for browsing air quality records."""

    list_display = (
        "id",
        "aqi",
        "pm10",
        "pm2_5",
        "temperature",
        "health_impact_class",
        "created_at",
    )
    list_filter = ("health_impact_class",)
    search_fields = ("id",)
    readonly_fields = ("created_at",)
