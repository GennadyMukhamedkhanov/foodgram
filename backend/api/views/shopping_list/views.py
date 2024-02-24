from django.http import FileResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
import base64

from api.serializers.shopping_list.serializers import (SearchObjectrRecipe,
                                                       ShoppingListAddSerializer,
                                                       ShoppingListDeleteSerializer,
                                                       RecipeSerializer,
                                                       SearchRecipe)
from recipes.models import Recipe, ShoppingList, IngredientWithAmount


class ShoppingListAddDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        recipe = SearchObjectrRecipe(
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
        recipe = SearchRecipe(
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


class DownloadShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        shoppings = ShoppingList.objects.filter(user=request.user).values_list(
            'recipe', flat=True)
        recipes = Recipe.objects.filter(id__in=shoppings)
        ingredient_dict = {}

        for recipe in recipes:
            ingredient_with_amount = recipe.ingredients_related_name.all()
            for rec in ingredient_with_amount:
                if rec.ingredient.name in ingredient_dict:
                    ingredient_dict[rec.ingredient.name][0] = \
                        ingredient_dict[rec.ingredient.name][0] + rec.amount
                else:
                    ingredient_dict[rec.ingredient.name] = [rec.amount,
                                                            rec.ingredient.measurement_unit]

        with open("list_shopping.txt", "w") as file:
            for ingredient in ingredient_dict:
                file.write(
                    f'{ingredient} - {ingredient_dict[ingredient][0]} - {ingredient_dict[ingredient][1]}\n'
                )


        short_report = open("list_shopping.txt", 'rb')

        report_encoded = base64.b64encode(short_report.read())
        return Response(report_encoded)




        #short_report = open("list_shopping.pdf", 'b', encoding='utf-8')
        #report_encoded = base64.b64encode(short_report.read())
        #return FileResponse(short_report)
        #return Response(short_report, headers={'Content-type': 'text/plain'})

# Todo values_list


# Todo как отдавать в ответ файл не создавая его на комп
