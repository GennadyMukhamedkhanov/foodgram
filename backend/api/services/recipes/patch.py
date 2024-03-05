from django import forms
from functools import lru_cache
from service_objects.fields import ModelField, ListField
from service_objects.services import Service
from api.serializers.recipes.creating_recipe_serializers import ImgSerializer
from recipes.models import Recipe, IngredientWithAmount, Ingredient, Tag
from users.models import User



class RecipesPatchService(Service):
    id = forms.IntegerField()
    ingredients = ListField()
    tags = ListField()
    image = forms.CharField()
    name = forms.CharField()
    text = forms.CharField()
    cooking_time = forms.IntegerField()
    author = ModelField(User)

    def process(self):
        recipe = self.get_recipe()
        self.patch_recipe(recipe)
        self.delete_old_tags(recipe)
        self.add_new_tags(recipe)
        self.delete_old_ingredients(recipe)
        self.add_new_ingredients(recipe)

        return recipe

    @lru_cache()
    def get_recipe(self):
        return Recipe.objects.get(id=self.cleaned_data['id'])

    def patch_recipe(self, recipe):
        recipe.image = self.base64_image()
        recipe.name = self.cleaned_data['name']
        recipe.text = self.cleaned_data['text']
        recipe.author = self.cleaned_data['author']
        recipe.cooking_time = self.check_positive_cooking_time(recipe)
        recipe.save()

    def delete_old_tags(self, recipe):
        for old_tags in recipe.tags.all():
            recipe.tags.remove(old_tags)

    def add_new_tags(self, recipe):
        for tag_id in self.check_tag_unique():
            tag_obj = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag_obj)

    def delete_old_ingredients(self, recipe):
        for old_ingredients in IngredientWithAmount.objects.filter(
                recipe=recipe):
            old_ingredients.delete()

    def add_new_ingredients(self, recipe):
        for ingr in self.check_ingredient_unique():
            IngredientWithAmount.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingr.get('id')),
                amount=ingr.get('amount')
            )

    @lru_cache()
    def check_ingredient_unique(self):
        list_id = [id_ingr['id'] for id_ingr in
                   self.cleaned_data['ingredients']]
        if len(list_id) != len(set(list_id)):
            raise ('The ingredients are specified incorrectly')
        return self.cleaned_data['ingredients']

    def check_tag_unique(self):
        list_tag = self.cleaned_data['tags']
        if len(list_tag) != len(set(list_tag)) or len(list_tag) < 0:
            raise ('The tag are specified incorrectly')
        return list_tag

    def check_positive_cooking_time(self, recipe):
        cooking_time = self.cleaned_data.get('cooking_time',
                                             recipe.cooking_time)
        if cooking_time < 1:
            raise ('The number must be greater than zero')
        return cooking_time

    def base64_image(self):
        serializer_base64 = ImgSerializer(
            data={'image': self.cleaned_data['image']})
        serializer_base64.is_valid(raise_exception=True)
        return serializer_base64.validated_data['image']

