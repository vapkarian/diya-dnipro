from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse
from django.db import models
from django.templatetags.static import static
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from sortedm2m.fields import SortedManyToManyField


from diya_dnipro.types import Url


__all__ = [
    'Category', 'Article', 'TeamMember', 'Document', 'Contact',
]


class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='Назва')
    url = models.CharField(max_length=128, verbose_name='Посилання')
    members = SortedManyToManyField('TeamMember', related_name='categories', blank=True,
                                    verbose_name='Персони')
    documents = SortedManyToManyField('Document', related_name='categories', blank=True,
                                      verbose_name='Документи')

    class Meta:
        verbose_name = 'запис категорії'
        verbose_name_plural = 'Категорії'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> Url:
        return reverse('news:category', args=(self.url,))


class Article(models.Model):
    category = models.ForeignKey('Category', related_name='articles', verbose_name='Категорія')
    title = models.TextField(verbose_name='Назва')
    image = models.ImageField(upload_to='uploads/', null=True, blank=True, verbose_name='Основне зображення до статті',
                              help_text=mark_safe('Якщо не обрано, буде використано стандартне зображення.'))
    text = RichTextUploadingField(verbose_name='Текст новини')
    created = models.DateTimeField(default=datetime.now, verbose_name='Дата розміщення')
    is_top = models.BooleanField(default=False, verbose_name='Додати до топу?')
    is_active = models.BooleanField(default=True, verbose_name='Відображати?')

    class Meta:
        verbose_name = 'запис новини'
        verbose_name_plural = 'Новини'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> Url:
        return reverse('news:article', args=(self.id,))

    @cached_property
    def top_thumbnail(self) -> Url:
        if self.image:
            url = get_thumbnailer(self.image)['top'].url
        else:
            url = static('news/img/top-thumbnail-default.jpg')
        return url

    @cached_property
    def preview_thumbnail(self) -> Url:
        if self.image:
            url = get_thumbnailer(self.image)['preview'].url
        else:
            url = static('news/img/preview-thumbnail-default.png')
        return url


class TeamMember(models.Model):
    name = models.CharField(max_length=128, verbose_name="Ім'я")
    position = models.CharField(max_length=128, verbose_name='Посада')
    photo = models.ImageField(upload_to='photos/', verbose_name='Світлина')
    bio = models.TextField(blank=True, verbose_name='Анкета')

    class Meta:
        verbose_name = 'запис персони'
        verbose_name_plural = 'Персони'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> Url:
        return reverse('news:member', args=(self.id,))


class Document(models.Model):
    title = models.TextField(verbose_name='Назва')
    description = models.TextField(verbose_name='Опис', blank=True)
    url = models.URLField(verbose_name='Посилання')

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'Документи'

    def __str__(self) -> str:
        return self.title


class Contact(models.Model):
    title = models.CharField(max_length=32)
    phones = models.TextField()

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'Контакти'

    def __str__(self) -> str:
        return self.title
