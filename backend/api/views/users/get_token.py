from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.serializers.users.serializers import (TokenSerializer)


class TokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['user']
        token = Token.objects.filter(user=obj)
        if not token.exists():
            token = Token.objects.create(user=obj)
        else:
            token = token.first()

        return Response({
            'Token': token.key
        },
            status=status.HTTP_201_CREATED)
