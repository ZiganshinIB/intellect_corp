from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        label=False,
        required=True,
        error_messages={'required': 'Укажите имя'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя',
                'class': 'form-control',
            })
    )
    last_name = forms.CharField(
        max_length=100,
        label=False,
        required=True,
        error_messages={'required': 'Укажите фамилию'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия',
                'class': 'form-control',
            }))
    surname = forms.CharField(
        label=False,
        max_length=100,
        required=True,
        error_messages={'required': 'Укажите отчество'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Отчество',
                'class': 'form-control',
            })
    )

    birthday = forms.DateField(
        label=False,
        required=True,
        error_messages={'required': 'Укажите дату рождения'},
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Дата рождения',
                'class': 'form-control',
            })
    )

    telephone = PhoneNumberField(
        label=False,
        required=True,
        error_messages={'required': 'Укажите номер телефона'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Номер телефона',
                'class': 'form-control',
            })
    )

    data_start_work = forms.DateField(
        label=False,
        required=True,
        error_messages={'required': 'Укажите дату начала работы'},
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Дата начала работы',
                'class': 'form-control',
            })
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'surname']
