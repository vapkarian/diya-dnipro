from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


__all__ = [
    'CustomUserCreationForm', 'CustomUserChangeForm,'
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
