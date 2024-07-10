from django import forms

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

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'surname']
