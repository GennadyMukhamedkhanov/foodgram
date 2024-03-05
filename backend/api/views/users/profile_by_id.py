from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.users.serializers import (UsersGetSerialisers)
from users.models import User


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        obj = get_object_or_404(User, id=kwargs['id'])

        return Response(
            UsersGetSerialisers(obj).data,
            status=status.HTTP_200_OK
        )
