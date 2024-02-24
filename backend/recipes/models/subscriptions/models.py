from django.db import models


class Subscription(models.Model):
    client = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='subscription_client'
    )
    author = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscription_author'
    )

    def __str__(self):
        return f'Пользователь - {self.client},  автор рецепта-{self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        app_label = 'recipes'
