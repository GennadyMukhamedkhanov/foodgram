from rest_framework.exceptions import ValidationError
from service_objects.services import Service
from django import forms
from recipes.models import Ingredient

class IngredientsGetService(Service):
    id = forms.IntegerField()

    def process(self):
        id = self.cleaned_data['id']
        ingredient = self.get_ingregients(id)
        self.check_ingredients(ingredient)

        return ingredient.first()

    @staticmethod
    def get_ingregients(pk):
        return Ingredient.objects.filter(id=pk)

    @staticmethod
    def check_ingredients(ingredient):
        if not ingredient.exists():
            raise ValidationError('The object was not found')
