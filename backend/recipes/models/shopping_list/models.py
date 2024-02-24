from django.db import models


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        to='Recipe',
        verbose_name='Рецепт',
        related_name='shoppings_lists',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to='users.User',
        verbose_name='Пользователь',
        related_name='shoppings',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipe}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        app_label = 'recipes'
