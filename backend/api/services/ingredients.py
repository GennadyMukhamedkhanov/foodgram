from rest_framework.exceptions import ValidationError
from service_objects.services import Service
from django import forms

from api.serializers.ingredients.serializers import IngredientSerialisers
from recipes.models.ingredient.models import Ingredient


class IngredientsListService(Service):
    search = forms.CharField(required=False)

    def process(self):
        search = self.cleaned_data['search']
        if search == None:
            ingredients = Ingredient.objects.all()
        else:
            ingredients = Ingredient.objects.filter(name__startswith=search)

        return ingredients


class IngredientsGetService(Service):
    id = forms.IntegerField()

    def process(self):
        id = self.cleaned_data['id']
        ingredient = Ingredient.objects.filter(id=id)
        if not ingredient.exists():
            raise ValidationError('The object was not found')

        return ingredient
