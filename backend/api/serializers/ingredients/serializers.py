from rest_framework import serializers
from recipes.models.ingredient.models import Ingredient


class IngredientSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'name',

        )
