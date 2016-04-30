from django.core.urlresolvers import reverse
from django.db import models

from diya_dnipro.types import Url


__all__ = [
    'Category', 'Item',
]


class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='Назва')
    image = models.ImageField(upload_to='shop/', verbose_name='Зображення')
    url = models.CharField(max_length=128, verbose_name='Посилання')

    class Meta:
        verbose_name = 'запис категорії'
        verbose_name_plural = 'Категорії'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> Url:
        return reverse('shop:category', args=(self.url,))


class Item(models.Model):
    category = models.ForeignKey('Category', related_name='items', verbose_name='Категорія')
    title = models.TextField(verbose_name='Назва')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Ціна')
    short_description = models.TextField(verbose_name='Короткий опис', blank=True)
    long_description = models.TextField(verbose_name='Повний опис', blank=True)
    image = models.ImageField(upload_to='shop/', verbose_name='Зображення')
    is_best = models.BooleanField(default=False, verbose_name='Показувати як кращий товар?')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> Url:
        return reverse('shop:item', args=(self.id,))
