from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from diya_dnipro.accounts.models import *
from diya_dnipro.accounts.tasks import send_mail
from diya_dnipro.misc.models import SiteSetting


__all__ = [
    'CustomUserCreationForm', 'CustomUserChangeForm', 'FeedbackForm',
]


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Паролі не співпадають',
    }
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class FeedbackForm(forms.ModelForm):
    email2 = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field_name in self._meta.fields:
            field = self.fields[field_name]
            field.widget.attrs['placeholder'] = field.label + ' *'

    def clean_email2(self) -> str:
        email2 = self.cleaned_data.get('email2')
        if email2:
            raise forms.ValidationError("Некоректний формат")
        return email2

    def send_mail(self) -> None:
        emails = [elem[1] for elem in settings.ADMINS]
        emails.append(SiteSetting.get_value('mail_url', ''))
        data = {
            'name': self.instance.name,
            'email': self.instance.email,
            'message': self.instance.message,
            'created': self.instance.created,
        }
        send_mail.delay(emails, 'Повідомлення', 'emails/feedback.txt', extra_context=data,
                        reply_to=(self.instance.name, self.instance.email))
