from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from worker.models import Profile, Department

from phonenumber_field.formfields import PhoneNumberField


class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'required': 'Пожалуйста, введите пароль.',
        },
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        print(password)
        if len(password) < 8:
            raise ValidationError(_('Пароль должен содержать не менее 8 символов.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Пароль должен содержать хотя бы одну цифру.'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Пароль должен содержать хотя бы одну букву.'))
        if not any(char in '!@#$%^&*()' for char in password):
            raise ValidationError(_('Пароль должен содержать хотя бы один специальный символ.'))
        return password
