from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.ingredients.serializers import IngredientSerialisers
from api.services.ingredients.get import IngredientsGetService


class IngredientsGetView(APIView):
    def get(self, request, **kwargs):
        try:
            ingredients = IngredientsGetService.execute(kwargs)
            return Response(IngredientSerialisers(ingredients).data)
        except ValidationError as error:
            return Response({
                'error': error.detail
            },
                status=status.HTTP_404_NOT_FOUND)
