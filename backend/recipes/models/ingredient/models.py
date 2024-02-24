from django.db import models


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=10)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        app_label = 'recipes'
