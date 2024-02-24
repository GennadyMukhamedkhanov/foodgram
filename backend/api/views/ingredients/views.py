from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.ingredients.serializers import IngredientSerialisers
from api.services.ingredients import IngredientsListService, IngredientsGetService


class IngredientsListView(APIView):
    def get(self, request):
        ingredients = IngredientsListService.execute(request.data)
        serializer = IngredientSerialisers(ingredients, many=True).data
        return Response(serializer)


class IngredientsGetView(APIView):
    def get(self, request, **kwargs):
        try:
            ingredients = IngredientsGetService.execute(kwargs)
            serializer = IngredientSerialisers(ingredients.first()).data
            return Response(serializer)
        except ValidationError as error:
            return Response({
                'error': error.detail
            },
                status=status.HTTP_404_NOT_FOUND)
