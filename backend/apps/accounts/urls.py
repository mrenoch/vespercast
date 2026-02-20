from django.urls import path
from .views import UserLocationListView

urlpatterns = [
    path("locations/", UserLocationListView.as_view(), name="user-location-list"),
]
