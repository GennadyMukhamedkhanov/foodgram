from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.users.serializers import (TokenObject)


class TokenLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TokenObject(data={}, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['obj_token']
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
