from service_objects.services import Service
from django import forms
from recipes.models import Ingredient


class IngredientsGetService(Service):
    id = forms.IntegerField()

    def process(self):
        return self._ingredient

    @property
    def _ingredient(self):
        ingredients = Ingredient.objects.filter(id=self.cleaned_data['id'])
        if not ingredients.exists():
            raise ValueError("Not found")
        return ingredients.first()
