from django import forms
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile, Department


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

    department = forms.ModelChoiceField(
        label='Отдел',
        queryset=Department.objects.all(),
        required=True,
        error_messages={'required': 'Укажите отдел'},
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    birthday = forms.DateField(
        label='Дата рождения',
        required=True,
        error_messages={'required': 'Укажите дату рождения'},
        widget=forms.DateInput(
            attrs={
                'type': 'date',
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
        label='Дата начала работы',
        required=True,
        error_messages={'required': 'Укажите дату начала работы'},
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'Дата начала работы',
                'class': 'form-control',
            })
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'surname',
                  'department', 'position',
                  'birthday', 'telephone', 'data_start_work',
                  'photo']

        widgets = {
            'position': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_birthday(self):
        super().clean()
        birthday = self.cleaned_data['birthday']
        if birthday > timezone.datetime.now().date():
            raise forms.ValidationError('Дата рождения не может быть больше текущей')
        return birthday

    def clean_data_start_work(self):
        super().clean()
        data_start_work = self.cleaned_data['data_start_work']
        if data_start_work < timezone.now().date():
            raise forms.ValidationError('Дата начала работы не может быть меньше текущей')
        return data_start_work

