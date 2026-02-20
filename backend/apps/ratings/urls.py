from django.urls import path
from .views import RatingCreateView

urlpatterns = [
    path("", RatingCreateView.as_view(), name="rating-create"),
]
