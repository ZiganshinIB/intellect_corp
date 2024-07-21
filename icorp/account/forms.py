from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.utils import timezone

from phonenumber_field.formfields import PhoneNumberField
from .form_field import UsernameField


UserModel = get_user_model()


class UserLoginForm(forms.Form):
    username = UsernameField(
        required=True,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-4 py-2  px-2 border-1',
            'placeholder': 'Логин',
            'name': 'username'
        })
    )
    password = forms.CharField(
        required=True,
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-4 py-2  px-2 border-1',
            'placeholder': 'Пароль',
            'name': 'password'
        })
    )

    error_messages = {
        "invalid_login": gettext_lazy(
            "Пожалуйста, введите правильный  %(username)s и пароль. Обратите внимание, что оба"
            "поля могут быть чувствительны к регистру."
        ),
        "inactive": gettext_lazy("Этот аккаунт заблокирован."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": "Логин"},
        )
