from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.users.serializers import (UsersGetSerialisers)


class PersonalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = request.user
        serializer = UsersGetSerialisers(instance).data
        return Response(serializer, status=status.HTTP_200_OK)
