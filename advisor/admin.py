from django.contrib import admin
from .models import AirQualityRecord

@admin.register(AirQualityRecord)
class AirQualityRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pm2_5",
        "ozone",
        "temperature",
        "humidity",
        "aqi_category",
        "created_at",
    )
    list_filter = ("aqi_category", "created_at")
    search_fields = ("id", "aqi_category")
    readonly_fields = ("created_at",)
