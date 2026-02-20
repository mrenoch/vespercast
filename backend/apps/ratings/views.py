from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SunsetRating
from .serializers import SunsetRatingSerializer


class RatingCreateView(APIView):
    """POST /api/v1/ratings/ — submit a 1–5 star rating."""

    def post(self, request):
        ser = SunsetRatingSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        rating = SunsetRating.objects.create(
            forecast=ser.validated_data["forecast"],
            user=user,
            score=ser.validated_data["score"],
            comment=ser.validated_data.get("comment", ""),
        )
        return Response(SunsetRatingSerializer(rating).data, status=status.HTTP_201_CREATED)
