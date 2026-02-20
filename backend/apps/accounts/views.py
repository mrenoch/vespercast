from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserLocation
from .serializers import UserLocationSerializer


class UserLocationListView(APIView):
    """GET /api/v1/accounts/locations/ — user's saved locations."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved = UserLocation.objects.filter(user=request.user).select_related("location")
        return Response(UserLocationSerializer(saved, many=True).data)
