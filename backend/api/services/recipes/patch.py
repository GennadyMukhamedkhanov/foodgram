from django import forms
from functools import lru_cache

from rest_framework.exceptions import ValidationError
from service_objects.fields import ModelField, ListField
from service_objects.services import Service
from api.serializers.recipes.creating_recipe_serializers import ImgSerializer
from recipes.models import Recipe, IngredientWithAmount, Ingredient, Tag
from users.models import User


class RecipesPatchService(Service):
    id = forms.IntegerField()
    ingredients = ListField()
    tags = ListField()
    image = forms.CharField()
    name = forms.CharField()
    text = forms.CharField()
    cooking_time = forms.IntegerField()
    author = ModelField(User)

    def process(self):
        self.recipe = self.get_recipe()
        self.patch_recipe()
        self.delete_old_tags()
        self.add_new_tags()
        self.delete_old_ingredients()
        self.add_new_ingredients()

        return self.recipe

    @lru_cache()
    def get_recipe(self):
        return Recipe.objects.get(id=self.cleaned_data['id'])

    def patch_recipe(self):
        self.recipe.image = self.base64_image()
        self.recipe.name = self.cleaned_data['name']
        self.recipe.text = self.cleaned_data['text']
        self.recipe.author = self.cleaned_data['author']
        self.recipe.cooking_time = self.check_positive_cooking_time(self.recipe)
        self.recipe.save()

    def delete_old_tags(self):
        for old_tags in self.recipe.tags.all():
            self.recipe.tags.remove(old_tags)

    def add_new_tags(self):
        for tag_id in self.check_tag_unique():
            tag_obj = Tag.objects.get(id=tag_id)
            self.recipe.tags.add(tag_obj)

    def delete_old_ingredients(self):
        for old_ingredients in IngredientWithAmount.objects.filter(
                recipe=self.recipe):
            old_ingredients.delete()

    def add_new_ingredients(self):
        for ingredient in self.check_ingredient_unique():
            IngredientWithAmount.objects.create(
                recipe=self.recipe,
                ingredient=Ingredient.objects.get(id=ingredient.get('id')),
                amount=ingredient.get('amount')
            )

    @lru_cache()
    def check_ingredient_unique(self):
        list_id = [
            ingredient['id'] for ingredient in self.cleaned_data['ingredients']
        ]
        if len(list_id) != len(set(list_id)):
            raise ValidationError('The ingredients are specified incorrectly')
        return self.cleaned_data['ingredients']

    def check_tag_unique(self):
        list_tag = self.cleaned_data['tags']
        if len(list_tag) != len(set(list_tag)) or len(list_tag) < 0:
            raise ('The tag are specified incorrectly')
        return list_tag

    def check_positive_cooking_time(self):
        cooking_time = self.cleaned_data.get(
            'cooking_time', self.recipe.cooking_time
        )
        if cooking_time < 1:
            raise ValidationError('The number must be greater than zero')
        return cooking_time

    def base64_image(self):
        serializer_base64 = ImgSerializer(
            data={'image': self.cleaned_data['image']}
        )
        serializer_base64.is_valid(raise_exception=True)
        return serializer_base64.validated_data['image']
