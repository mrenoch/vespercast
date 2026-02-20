from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "lat", "lng", "elevation", "created_at"]
    search_fields = ["name"]
