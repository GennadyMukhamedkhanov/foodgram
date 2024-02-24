from django.db import models


class Favourite(models.Model):
    recipe = models.ForeignKey(to='Recipe', verbose_name='Рецепт',
                                related_name='favourites_recipes',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(to='users.User', verbose_name='Пользователь',
                             related_name='favourites',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        app_label = 'recipes'
