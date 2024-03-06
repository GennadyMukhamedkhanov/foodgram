from service_objects.services import Service
from django import forms

from recipes.models import Ingredient


class IngredientsListService(Service):
    name = forms.CharField(required=False)

    def process(self):
        if self.cleaned_data['name'] is None:
            ingredients = Ingredient.objects.all()
        else:
            ingredients = Ingredient.objects.filter(
                name__startswith=self.cleaned_data['name']
            )
        return ingredients
