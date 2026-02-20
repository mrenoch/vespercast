from django.urls import path
from .views import GeocodeView, LocationListCreateView

urlpatterns = [
    path("geocode/", GeocodeView.as_view(), name="location-geocode"),
    path("", LocationListCreateView.as_view(), name="location-list-create"),
]
