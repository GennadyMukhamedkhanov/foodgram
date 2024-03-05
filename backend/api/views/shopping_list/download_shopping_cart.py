from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from recipes.models import Recipe, ShoppingList


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

        shopping_list_str = ""
        for ingredient in ingredient_dict:
            shopping_list_str += f'{ingredient} - {ingredient_dict[ingredient][0]} - {ingredient_dict[ingredient][1]}\n'
        response = HttpResponse(shopping_list_str, content_type="text/plain")
        response[
            'Content-Disposition'] = 'attachment; filename=list_shopping.txt'
        return response
