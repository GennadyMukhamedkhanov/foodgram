from rest_framework import serializers

from recipes.models import Recipe, Favourite
from recipes.models.ingredient.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Favourite
        fields = (

            "id",
            "name",
            "image",
            "cooking_time"
        )


class FavoriteValidationAddSerializer(serializers.Serializer):
    pass
