
from service_objects.fields import ModelField, ListField
from service_objects.services import Service
from django import forms
from api.serializers.recipes.creating_recipe_serializers import ImgSerializer
from recipes.models import IngredientWithAmount, Ingredient, Recipe, Tag
from users.models import User


class RecipesAddService(Service):
    ingredients = ListField()
    tags = ListField()
    image = forms.CharField()
    name = forms.CharField()
    text = forms.CharField()
    cooking_time = forms.IntegerField()
    author = ModelField(User)

    def process(self):
        recipe = self.create_recipe()
        self.add_tags_in_recipe(recipe)
        self.add_data_in_model_ingredient_with_amount(recipe)

        return recipe

    def base64_image(self):
        serializer_base64 = ImgSerializer(
            data={'image': self.cleaned_data['image']})
        serializer_base64.is_valid(raise_exception=True)
        return serializer_base64.validated_data['image']

    def add_data_in_model_ingredient_with_amount(self, recipe):
        for ingredient in self.check_ingredient_unique():
            IngredientWithAmount.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )

    def create_recipe(self):
        return Recipe.objects.create(
            image=self.base64_image(),
            name=self.cleaned_data['name'],
            text=self.cleaned_data['text'],
            author=self.cleaned_data['author'],
            cooking_time=self.check_positive_cooking_time()
        )

    def add_tags_in_recipe(self, recipe):
        for tag in self.cleaned_data['tags']:
            tag_obj = Tag.objects.get(id=tag)
            recipe.tags.add(tag_obj)

    def check_ingredient_unique(self):
        list_id = [id_ingr['id'] for id_ingr in
                   self.cleaned_data['ingredients']]
        if len(list_id) != len(set(list_id)):
            raise ('The ingredients are specified incorrectly')
        return self.cleaned_data['ingredients']

    def check_tag_unique(self, list_tag):
        if len(list_tag) != len(set(list_tag)) or len(list_tag) < 0:
            raise ('The tag are specified incorrectly')
        return list_tag

    def check_positive_cooking_time(self):
        if self.cleaned_data['cooking_time'] < 1:
            raise ('The number must be greater than zero')
        return self.cleaned_data['cooking_time']