from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Subscription, Favourite, Recipe, Ingredient
from rest_framework.generics import get_object_or_404
from users.models import User


class RecipesShortSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipe = Recipe.objects.filter(
            author=obj.author
        )[:self.context['recipes_limit']]
        return RecipesShortSerialisers(recipe, many=True).data
# Todo можно ли так делать?
    def get_recipes_count(self, obj):
        queru = self.get_recipes(obj)
        return len(queru)

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count'

        )


class SubscribeValidationSerializers(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        author = get_object_or_404(User, id=attrs['id'])
        if author == self.context['request'].user:
            raise ValidationError(
                'Подписываться на себя запрещено')

        find_object = Subscription.objects.filter(
            client=self.context['request'].user,
            author=author)
        if find_object.exists():
            raise ValidationError('Вы уже подписаны на данного автора')
        attrs['author'] = author
        return attrs


class SubscribeValidationDeleteSerializers(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        author = get_object_or_404(User, id=attrs['id'])
        if author == self.context['request'].user:
            raise ValidationError(
                'Отписаться от себя нельзя')
        find_object = Subscription.objects.filter(
            client=self.context['request'].user,
            author=author)
        if not find_object.exists():
            raise ValidationError('Вы не подписаны на данного автора')
        attrs['subscribe'] = find_object.first()
        return attrs

