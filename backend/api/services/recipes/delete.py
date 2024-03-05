
from rest_framework.generics import get_object_or_404
from service_objects.services import Service
from django import forms
from recipes.models import Recipe


class RecipesDeleteService(Service):
    id = forms.IntegerField()

    def process(self):
        recipe = get_object_or_404(Recipe, id=self.cleaned_data['id'])
        recipe.delete()
