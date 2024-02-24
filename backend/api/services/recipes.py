from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField, DictField, ListField
from service_objects.services import Service
from django import forms
from functools import lru_cache
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe, IngredientWithAmount, Ingredient, Tag
from users.models import User


class RecipesListService(Service):

    def process(self):
        recipes = Recipe.objects.all()
        return recipes


class RecipesAddService(Service):
    ingredients = ListField()
    tags = ListField()
    image = forms.CharField()
    name = forms.CharField()
    text = forms.CharField()
    cooking_time = forms.IntegerField()
    author = ModelField(User)

    # Todo конвентировать фото

    def process(self):
        ingredients = self.check_ingredient_unique(
            self.cleaned_data['ingredients'])
        tags = self.check_tag_unique(self.cleaned_data['tags'])
        image = self.cleaned_data['image']
        name = self.cleaned_data['name']
        text = self.cleaned_data['text']
        cooking_time = self.check_positive_cooking_time(
            self.cleaned_data['cooking_time'])
        author = self.cleaned_data['author']

        recipe = Recipe.objects.create(

            image=image,
            name=name,
            text=text,
            author=author,
            cooking_time=cooking_time
        )
        for tag in tags:
            tag_obj = Tag.objects.get(id=tag)

            recipe.tags.add(tag_obj)

        for ingr in ingredients:
            IngredientWithAmount.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingr['id']),
                amount=ingr['amount']
            )

        return recipe

    def check_ingredient_unique(self, list_ingredient):
        list_id = [id_ingr['id'] for id_ingr in list_ingredient]
        if len(list_id) != len(set(list_id)):
            raise ('The ingredients are specified incorrectly')
        return list_ingredient

    def check_tag_unique(self, list_tag):
        if len(list_tag) != len(set(list_tag)) or len(list_tag) < 0:
            raise ('The tag are specified incorrectly')
        return list_tag

    def check_positive_cooking_time(self, time):
        if time < 1:
            raise ('The number must be greater than zero')
        return time


class RecipesPatchService(Service):
    id = forms.IntegerField()
    ingredients = ListField()
    tags = ListField()
    image = forms.CharField()
    name = forms.CharField()
    text = forms.CharField()
    cooking_time = forms.IntegerField()
    author = ModelField(User)

    # Todo конвентировать фото

    def process(self):
        ingredients = self.check_ingredient_unique(
            self.cleaned_data['ingredients'])
        tags = self.check_tag_unique(self.cleaned_data['tags'])
        image = self.cleaned_data['image']
        name = self.cleaned_data['name']
        text = self.cleaned_data['text']
        cooking_time = self.check_positive_cooking_time(
            self.cleaned_data['cooking_time'])
        author = self.cleaned_data['author']
        id = self.cleaned_data['id']
        recipe = self.get_recipe(id)
        self.patch_recipe(recipe, image, name, text, author, cooking_time)
        self.delete_old_tags(recipe)
        self.add_new_tags(recipe, tags)
        self.delete_old_ingredients(recipe)
        self.add_new_ingredients(recipe, ingredients)

        return recipe

    def get_recipe(self, id):
        return Recipe.objects.get(id=id)

    def patch_recipe(self, recipe, image, name, text, author, cooking_time):
        recipe.image = image
        recipe.name = name
        recipe.text = text
        recipe.author = author
        recipe.cooking_time = cooking_time
        recipe.save()

    def delete_old_tags(self, recipe):
        for old_tags in recipe.tags.all():
            recipe.tags.remove(old_tags)

    def add_new_tags(self, recipe, tags):
        for tag_id in tags:
            tag_obj = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag_obj)

    def delete_old_ingredients(self, recipe):
        for old_ingredients in IngredientWithAmount.objects.filter(
                recipe=recipe):
            old_ingredients.delete()

    def add_new_ingredients(self, recipe, ingredients):
        for ingr in ingredients:
            IngredientWithAmount.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingr.get('id')),
                amount=ingr.get('amount')
            )

    def check_ingredient_unique(self, list_ingredient):
        list_id = [id_ingr['id'] for id_ingr in list_ingredient]
        if len(list_id) != len(set(list_id)):
            raise ('The ingredients are specified incorrectly')
        return list_ingredient

    def check_tag_unique(self, list_tag):
        if len(list_tag) != len(set(list_tag)) or len(list_tag) < 0:
            raise ('The tag are specified incorrectly')
        return list_tag

    def check_positive_cooking_time(self, time):
        if time < 1:
            raise ('The number must be greater than zero')
        return time


class RecipesDeleteService(Service):
    id = forms.IntegerField()

    def process(self):
        recipe = get_object_or_404(Recipe, id=self.cleaned_data['id'])
        recipe.delete()
