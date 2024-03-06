from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.ingredients.serializers import IngredientSerialisers
from api.services.ingredients.list import IngredientsListService


class IngredientsListView(APIView):
    def get(self, request):
        ingredients = IngredientsListService.execute(request.query_params)
        return Response(
            IngredientSerialisers(ingredients, many=True).data,
            status=status.HTTP_200_OK
        )
