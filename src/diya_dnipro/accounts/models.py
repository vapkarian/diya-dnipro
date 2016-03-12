from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


__all__ = [
    'User', 'Feedback', 'TrackingRecord',
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str = None, **extra_fields):  # TODO: add typing for User
        """
        Create and save a general user with the given credentials.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields):  # TODO: add typing for User
        """
        Create and save a super admin with the given credentials.
        """
        if extra_fields.setdefault('is_staff', True) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.setdefault('is_superuser', True) is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, blank=True, verbose_name='Ім’я')
    email = models.EmailField(unique=True, verbose_name='адреса електронної пошти', error_messages={
        'unique': 'Така адреса електронної пошти вже існує',
    })
    is_staff = models.BooleanField(default=False, verbose_name='Статус адміна',
                                   help_text='Визначає, що цей користувач має доступ до панелі адміністрування.')
    is_active = models.BooleanField(default=True, verbose_name='Активний',
                                    help_text='Визначає, що цей користувач не є заблокованим.')
    is_beta = models.BooleanField(default=False, verbose_name='Статус вибробувальника',
                                  help_text='Визначає, що цей користувач має доступ до тествого функционалу.')
    date_joined = models.DateTimeField(default=datetime.now, verbose_name='Дата першої появи')

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'запис користувача'
        verbose_name_plural = 'Користувачі'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        return self.name

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=64, verbose_name="Ім'я")
    email = models.EmailField(verbose_name='Адреса електронної пошти')
    message = models.TextField(verbose_name='Текст повідомлення')
    created = models.DateTimeField(default=datetime.now, verbose_name='Дата розміщення')

    class Meta:
        verbose_name = 'повідомлення'
        verbose_name_plural = 'Повідомлення'

    def __str__(self) -> str:
        return '{name} ({email})'.format(name=self.name, email=self.email)


class TrackingRecord(models.Model):
    ua_string = models.TextField(blank=True, verbose_name='User-Agent')
    ip = models.TextField(blank=True, db_index=True, verbose_name='IP адреса')
    referrer = models.TextField(blank=True, verbose_name='URL джерела запиту')
    browser_family = models.TextField(blank=True, db_index=True, verbose_name='Сімейство браузера')
    browser_version = models.TextField(blank=True, verbose_name='Версія браузера')
    os_family = models.TextField(blank=True, db_index=True, verbose_name='Сімейство операційної системи')
    os_version = models.TextField(blank=True, verbose_name='Версія операційної системи')
    device_brand = models.TextField(blank=True, db_index=True, verbose_name='Марка пристрою')
    device_family = models.TextField(blank=True, verbose_name='Сімейство пристрою')
    device_model = models.TextField(blank=True, verbose_name='Модель пристрою')
    coordinates = models.TextField(blank=True, verbose_name='Координати')
    city = models.TextField(blank=True, db_index=True, verbose_name='Місто')
    region = models.TextField(blank=True, verbose_name='Регіон')
    country = models.TextField(blank=True, db_index=True, verbose_name='Країна')
    created = models.DateTimeField(default=datetime.now, verbose_name='Дата розміщення')

    class Meta:
        verbose_name = 'запис відстеження'
        verbose_name_plural = 'Записи відстеження'

    def __str__(self) -> str:
        return '{ip} ({device} {os} {browser})'.format(ip=self.ip, device=self.device, os=self.os, browser=self.browser)

    @property
    def map_url(self) -> str:
        url = ''
        if self.coordinates:
            latitude, longitude = self.coordinates.split(',')
            url = 'http://www.gps-coordinates.net/latitude-longitude/{latitude}/{longitude}'.format(**locals())
        return url

    @staticmethod
    def _shorten_value(family: str, version: str) -> str:
        value = ''
        if family:
            value = family
            if version:
                value = '{value} {version}'.format(value=value, version=version)
        return value

    @property
    def browser(self) -> str:
        return self._shorten_value(self.browser_family, self.browser_version)

    @property
    def os(self) -> str:
        return self._shorten_value(self.os_family, self.os_version)

    @property
    def device(self) -> str:
        return self._shorten_value(self.device_brand, self.device_family)
