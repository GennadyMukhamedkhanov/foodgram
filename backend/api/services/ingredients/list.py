from service_objects.services import Service
from django import forms

from recipes.models import Ingredient



class IngredientsListService(Service):
    name = forms.CharField(required=False)

    def process(self):
        name = self.cleaned_data['name']
        if name == None:
            ingredients = Ingredient.objects.all()
        else:
            ingredients = Ingredient.objects.filter(name__startswith=name)

        return ingredients