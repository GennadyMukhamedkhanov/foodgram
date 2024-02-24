from rest_framework import serializers

from recipes.models import Recipe, IngredientWithAmount, Tag, Subscription
from users.models import User

class IngredientWithAmountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')

    class Meta:
        model = IngredientWithAmount
        fields = (
            'id',
            'amount'
        )

class CreatingRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ing_rec_queryset = IngredientWithAmount.objects.filter(recipe=obj)
        return IngredientWithAmountSerializer(ing_rec_queryset, many=True).data



    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )