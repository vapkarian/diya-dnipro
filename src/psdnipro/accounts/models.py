from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


__all__ = [
    'User', 'Feedback',
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a general user with the given credentials.

        :param str email: given email address
        :param str password: given raw password
        :param dict extra_fields: additional parameters of User model
        :rtype: psdnipro.accounts.models.User
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

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a super admin with the given credentials.

        :param str email: given email address
        :param str password: given raw password
        :param dict extra_fields: additional parameters of User model
        :rtype: psdnipro.accounts.models.User
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

    def __str__(self):
        return self.name

    def get_full_name(self):
        """
        Return name of user.

        :rtype: str
        """
        return self.name

    def get_short_name(self):
        """
        Return name of user.

        :rtype: str
        """
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=64, verbose_name="Ім'я")
    email = models.EmailField(verbose_name='Адреса електронної пошти')
    message = models.TextField(verbose_name='Текст повідомлення')
    created = models.DateTimeField(default=datetime.now, verbose_name='Дата розміщення')

    class Meta:
        verbose_name = 'повідомлення'
        verbose_name_plural = 'Повідомлення'

    def __str__(self):
        return '{name} ({email})'.format(name=self.name, email=self.email)
