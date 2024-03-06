from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.favorite.serializers import FavoriteSerializer
from api.services.favorites.add import FavoriteCreateService
from api.services.favorites.delete import FavoriteDeleteService


class FavoriteCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        result = FavoriteCreateService.execute({
            'user': request.user,
            'recipe_id': kwargs['id'],
        })
        return Response(
            FavoriteSerializer(result).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, **kwargs):
        FavoriteDeleteService.execute({
            'user': request.user,
            'recipe_id': kwargs['id'],
        })
        return Response(status=status.HTTP_204_NO_CONTENT)
