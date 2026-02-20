from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/locations/", include("apps.locations.urls")),
    path("api/v1/forecasts/", include("apps.forecasts.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path("api/v1/accounts/", include("apps.accounts.urls")),
]
