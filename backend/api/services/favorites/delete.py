from rest_framework.exceptions import ValidationError
from service_objects.fields import ModelField
from service_objects.services import Service
from django import forms
from rest_framework.generics import get_object_or_404
from functools import lru_cache

from recipes.models import Favourite, Recipe
from users.models import User


class FavoriteDeleteService(Service):
    user = ModelField(User)
    recipe_id = forms.IntegerField()

    def process(self):
        self.favorite = self.check_obj_favorite()
        self.delete_favorite()
        return self

    def delete_favorite(self):
        self.favorite.delete()

    def get_recipe_object(self):
        return get_object_or_404(
            Recipe, id=self.cleaned_data['recipe_id']
        )

    def check_obj_favorite(self):
        favorite = Favourite.objects.filter(
            recipe=self.get_recipe_object(),
            user=self.cleaned_data['user']
        )
        if not favorite.exists():
            raise ValidationError('Рецепта нет в избранном')
        return favorite.first()
