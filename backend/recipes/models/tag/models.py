from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    color = ColorField(default='#FF0000', verbose_name='Цвет')
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    def __str__(self):
        return f'{self.name}-{self.color}-{self.slug}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        app_label = 'recipes'
