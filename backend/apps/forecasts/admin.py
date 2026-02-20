from django.contrib import admin
from .models import SunsetForecast


@admin.register(SunsetForecast)
class SunsetForecastAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "forecast_date", "quality_score", "quality_label", "fetched_at"]
    list_filter = ["quality_label"]
    search_fields = ["location__name"]
