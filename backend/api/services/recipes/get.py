from service_objects.services import Service
from django import forms
from rest_framework.generics import get_object_or_404

from recipes.models import Recipe


class RecipeGetService(Service):
    id = forms.IntegerField()

    def process(self):
        return get_object_or_404(Recipe, id=self.cleaned_data['id'])
