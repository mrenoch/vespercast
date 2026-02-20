from django.contrib import admin
from .models import SunsetRating


@admin.register(SunsetRating)
class SunsetRatingAdmin(admin.ModelAdmin):
    list_display = ["id", "forecast", "user", "score", "created_at"]
    list_filter = ["score"]
