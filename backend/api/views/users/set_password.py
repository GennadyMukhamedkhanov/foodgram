from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.users.serializers import (UserChangePassword)


class SetPasswordView(APIView):
    def post(self, request):
        serializer = UserChangePassword(data={
            'id': request.user.id,
            'current_password': request.data['current_password']
        })
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['id']
        obj.set_password(request.data['new_password'])
        obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
