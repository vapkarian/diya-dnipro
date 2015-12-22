from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.templatetags.static import static
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


__all__ = [
    'Image', 'Category', 'Article', 'TeamMember',
]


class Image(models.Model):
    note = models.TextField(blank=True, verbose_name='Нотатки')
    file = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='Зображення')

    class Meta:
        verbose_name = 'зображення'
        verbose_name_plural = 'Зображення'

    def __str__(self):
        return self.file.name

    @cached_property
    def url(self):
        return self.file.url

    @cached_property
    def preview(self):
        obj = '<a href="{url}" target="_blank"><img class="preview" src="{url}" width=200/></a>'.format(url=self.url)
        return mark_safe(obj)


class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='Назва')
    url = models.CharField(max_length=128, verbose_name='Посилання')

    class Meta:
        verbose_name = 'запис категорії'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news', args=(self.url,))


class Article(models.Model):
    DEFAULT_MAIN_IMAGE = static('news/img/default-preview.png')

    category = models.ForeignKey(Category, verbose_name='Категорія')
    title = models.TextField(verbose_name='Назва')
    main_image = models.ForeignKey(Image, null=True, blank=True, related_name='main_articles',
                                   verbose_name='Основне зображення до статті', help_text=
                                   mark_safe('Якщо не обрано, за замовчуванням використовується <a href="{}" '
                                             'target="_blank">стандартне зображення</a>.'.format(DEFAULT_MAIN_IMAGE)))
    text = models.TextField(verbose_name='Текст новини')
    images = models.ManyToManyField(Image, blank=True, related_name='articles',
                                    verbose_name='Додаткові зображення до статті')
    created = models.DateTimeField(default=datetime.now, verbose_name='Дата розміщення')
    is_top = models.BooleanField(default=False, verbose_name='Додати до топу?')
    top_image = models.ForeignKey(Image, null=True, blank=True, related_name='top_articles',
                                  verbose_name='Зображення для ТОПу', help_text='Оптимальний розмір - 727 x 378.')
    is_active = models.BooleanField(default=True, verbose_name='Показувати?')

    class Meta:
        verbose_name = 'запис новини'
        verbose_name_plural = 'Новини'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article', args=(self.id,))

    @cached_property
    def main_image_url(self):
        """
        Return url to the main image file if it exists, otherwise return default article image.

        :rtype: str
        """
        if self.main_image is not None:
            return self.main_image.url
        return self.DEFAULT_MAIN_IMAGE

    @cached_property
    def top_image_url(self):
        """
        Return url to the top image file if it exists and article is on TOP.

        :rtype: str
        """
        if self.top_image is not None:
            return self.top_image.url

    @cached_property
    def images_urls(self):
        """
        Return url to the top image file if it exists and article is on TOP.

        :rtype: list[str]
        """
        return [elem.url for elem in self.images.all()]


class TeamMember(models.Model):
    name = models.CharField(max_length=128, verbose_name="Ім'я")
    position = models.CharField(max_length=128, verbose_name='Посада')
    photo = models.ImageField(upload_to='photos/', verbose_name='Світлина')
    bio = models.TextField(blank=True, verbose_name='Анкета')
    category = models.ForeignKey(Category, verbose_name='Категорія')

    class Meta:
        verbose_name = 'запис персони'
        verbose_name_plural = 'Персони'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:member', args=(self.id,))
