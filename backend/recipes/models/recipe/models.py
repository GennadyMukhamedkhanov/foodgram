from django.db import models
from recipes.models.ingredient.models import Ingredient


class Recipe(models.Model):
    ingredients = models.ManyToManyField(to='Ingredient',
                                         verbose_name='Ингредиенты',
                                         through='IngredientWithAmount')
    tags = models.ManyToManyField(to='Tag', verbose_name='Тег',
                                  related_name='tags')
    image = models.ImageField(upload_to='service/', verbose_name='Изображение')
    name = models.CharField(max_length=30, verbose_name='Имя')
    text = models.TextField(blank=False, null=True,
                            verbose_name='Текст')
    cooking_time = models.IntegerField(verbose_name='Время')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='recipes')

    def __str__(self):
        return f'{self.ingredients}-{self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        app_label = 'recipes'


class IngredientWithAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_related_name')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Колличество')

    def __str__(self):
        return f'{self.recipe}-{self.ingredient}-{self.amount}'

    class Meta:
        verbose_name = 'Ингредиент с количеством'
        verbose_name_plural = 'Ингредиенты с количеством'
        app_label = 'recipes'
