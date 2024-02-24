from rest_framework import serializers

from recipes.models import Recipe, IngredientWithAmount, Tag, Subscription
from users.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name'
        )


class IngredientWithAmountSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientWithAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'

        )


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class RecipesListSerializers(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializers(many=True)
    author = AuthorSerializer()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        client = self.context['request'].user.id
        author = obj.author.id
        subscribed = Subscription.objects.filter(client=client, author=author)
        if not subscribed.exists():
            return False
        return True

    def get_ingredients(self, obj):
        ingr_with_amount = IngredientWithAmount.objects.filter(recipe=obj)
        serealizer = IngredientWithAmountSerializers(ingr_with_amount,
                                                     many=True).data

        return serealizer

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_subscribed'

        )
