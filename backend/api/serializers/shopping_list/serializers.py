from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from recipes.models import ShoppingList, Recipe
from functools import lru_cache


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingListAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = (
            'recipe',
            'user'
        )

    def create(self, validated_data):
        return ShoppingList.objects.create(**validated_data)


class ShoppingListDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = (
            'recipe',
            'user'
        )

    def create(self, validated_data):
        return ShoppingList.objects.create(**validated_data)


class SearchObjectrRecipe(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        self.find_obj_shopping_list()
        attrs['recipe'] = self.get_obj_recipe()
        return attrs

    def find_obj_shopping_list(self):
        search_obj = ShoppingList.objects.filter(
            recipe=self.get_obj_recipe(),
            user=self.context['user']
        )
        if search_obj.exists():
            raise ValidationError('Товар уже находится в вашей корзине')

    @lru_cache()
    def get_obj_recipe(self):
        return get_object_or_404(Recipe, id=self.initial_data['id'])
# Todo можно ли делать через initial_data?

class SearchRecipe(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        recipe = get_object_or_404(Recipe, id=attrs['id'])
        search_obj = ShoppingList.objects.filter(
            recipe=recipe,
            user=self.context['user']
        )
        if not search_obj.exists():
            raise ValidationError('Данного товара нет в вашей корзине')
        attrs['recipe'] = recipe
        attrs['search_obj'] = search_obj.first()
        return attrs
