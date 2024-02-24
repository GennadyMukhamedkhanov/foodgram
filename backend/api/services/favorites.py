from rest_framework.exceptions import ValidationError
from service_objects.fields import ModelField
from service_objects.services import Service
from django import forms
from rest_framework.generics import get_object_or_404
from functools import lru_cache

from recipes.models import Favourite, Recipe
from users.models import User


class FavoriteAddService(Service):
    user = ModelField(User)
    recipe_id = forms.IntegerField()

    def process(self):
        self.check_obj_favorite()
        return self.create_favorite()

    def create_favorite(self):
        favorite_obj = Favourite.objects.create(
            recipe=self.get_recipe_object(),
            user=self.cleaned_data['user'])
        return favorite_obj

    @lru_cache()
    def get_recipe_object(self):
        return get_object_or_404(Recipe,
                                 id=self.cleaned_data['recipe_id'])

    def check_obj_favorite(self):
        favorite = Favourite.objects.filter(
            recipe=self.get_recipe_object(),
            user=self.cleaned_data['user']
        )
        if favorite.exists():
            raise ValidationError('Рецепт уже в избранном')


class FavoriteDeleteService(Service):
    user = ModelField(User)
    recipe_id = forms.IntegerField()

    def process(self):
        self.check_obj_favorite()

        return 1

    @lru_cache()
    def get_recipe_object(self):
        return get_object_or_404(Recipe,
                                 id=self.cleaned_data['recipe_id'])

    def check_obj_favorite(self):
        favorite = Favourite.objects.filter(recipe=self.get_recipe_object(),
                                            user=self.cleaned_data['user'])
        if not favorite.exists():
            raise ValidationError('Рецепта нет в избранном')
        favorite.first().delete()
