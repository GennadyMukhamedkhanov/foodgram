
import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe, IngredientWithAmount, Tag, Subscription
import psycopg2
from PIL import Image

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

class ImgSerializer(serializers.Serializer):
    image = Base64ImageField(required=False)

