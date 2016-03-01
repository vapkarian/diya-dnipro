from fractions import Fraction

from django.core.cache import cache
from django.db import models


class SiteSetting(models.Model):
    """
    Key-value storage unit.
    """
    SECTIONS = (
        (0, 'Загальне'),
        (1, 'Зовнішні посилання'),
    )
    TYPES = (
        (0, 'Текст'),
        (1, 'Ціле число'),
        (2, 'Десятковий дріб'),
        (3, 'Натуральний дріб'),
    )
    key = models.CharField(unique=True, max_length=64, verbose_name='Ключ')
    value = models.CharField(max_length=128, verbose_name='Значення')
    description = models.TextField(blank=True, verbose_name='Опис')
    section = models.PositiveSmallIntegerField(choices=SECTIONS, verbose_name='Секція')
    type = models.PositiveSmallIntegerField(choices=TYPES, verbose_name='Тип')

    class Meta:
        verbose_name = 'Налаштування'
        verbose_name_plural = 'Налаштування'

    def __str__(self):
        return '{key} = {value}'.format(key=self.key, value=self.value)

    def save(self, *args, **kwargs):
        """
        Reset cached value of SiteSetting object.

        :param list args: arbitrary argument list
        :param dict kwargs: keyword arguments
        """
        cache.delete(SiteSetting.cached_key(self.key))
        return super(SiteSetting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Reset cached value of SiteSetting object.

        :param list args: arbitrary argument list
        :param dict kwargs: keyword arguments
        """
        cache.delete(SiteSetting.cached_key(self.key))
        return super(SiteSetting, self).delete(*args, **kwargs)

    @classmethod
    def cached_key(cls, key):
        """
        Form cached key for given raw key.

        :param str key: given raw key.
        :rtype: str
        """
        return 'misc:site_setting:{key}'.format(key=key)

    @classmethod
    def get_value(cls, key, default=None):
        """
        Get value for given key. If key doesn't exist, default will be return if it is present, otherwise DoesNotExist
        will be raised.

        :param str key: given key
        :param str|int|float|Fraction default: default value if key doesn't exist
        :rtype: str|int|float|Fraction
        """
        converters = {
            0: str,
            1: int,
            2: float,
            3: Fraction,
        }
        cached_key = SiteSetting.cached_key(key)
        obj = cache.get(cached_key, None)
        if obj is None:
            try:
                obj = SiteSetting.objects.get(key=key)
            except SiteSetting.DoesNotExist:
                if default is not None:
                    return default
                else:
                    raise
            else:
                cache.set(cached_key, obj)
        func = converters[obj.type]
        value = func(obj.value)
        return value
