from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.favorite.serializers import FavoriteSerializer
from api.services.favorites.add import FavoriteAddService
from api.services.favorites.delete import FavoriteDeleteService


class FavoriteAddDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        data = FavoriteAddService.execute({
            'user': request.user,
            'recipe_id': kwargs['id'],
        })
        serializer = FavoriteSerializer(data).data
        return Response(
            serializer,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, **kwargs):
        FavoriteDeleteService.execute({
            'user': request.user,
            'recipe_id': kwargs['id'],
        })
        return Response(status=status.HTTP_204_NO_CONTENT)

