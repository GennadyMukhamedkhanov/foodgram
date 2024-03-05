from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.shopping_list.serializers import (SearchObjectrRecipeSerializer,
                                                       ShoppingListAddSerializer,
                                                       ShoppingListDeleteSerializer,
                                                       RecipeSerializer,
                                                       SearchRecipeSerializer)


class ShoppingListAddDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        recipe = SearchObjectrRecipeSerializer(
            data=kwargs,
            context={'user': request.user}
        )
        recipe.is_valid(raise_exception=True)

        kwargs['recipe'] = recipe.validated_data['recipe'].id
        kwargs['user'] = request.user.id
        serializers = ShoppingListAddSerializer(data=kwargs)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            RecipeSerializer(serializers.validated_data['recipe']).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, **kwargs):
        recipe = SearchRecipeSerializer(
            data=kwargs,
            context={'user': request.user}
        )
        recipe.is_valid(raise_exception=True)
        kwargs['recipe'] = recipe.validated_data['recipe'].id
        kwargs['user'] = request.user.id
        serializers = ShoppingListDeleteSerializer(data=kwargs)
        serializers.is_valid(raise_exception=True)
        recipe.validated_data['search_obj'].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

