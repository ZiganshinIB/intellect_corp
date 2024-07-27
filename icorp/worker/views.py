from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import transliterate

from tasker.models import Task
from .models import Profile
from .forms import ProfileForm


def index(request):
    return render(request, 'worker/index.html', {'section': 'dashboard'})


def create_task_add_profile(request):
    """ Create task and add profile to it """
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Добавляем профиль
            # Имя пользователя профиля переводим из кириллицы в латын нижней регистрации
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_name = transliterate.translit(
                f"{first_name}.{last_name}",
                'ru',
                reversed=True).replace("'", "").replace("`", "")
            count = User.objects.filter(Q(username__startswith=user_name)).count()
            if count > 0:
                user_name = f"{user_name}{count}"
            new_user = User.objects.create_user(
                username=user_name,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )
            new_user.set_password("QwerTy123!)(*")
            new_user.save()
            profile = Profile.objects.create(
                user=new_user,
                patronymic=form.cleaned_data['surname'] if form.cleaned_data['surname'] else None,  # patronymic
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'],
                phone=form.cleaned_data['telephone'],
                data_start_work=form.cleaned_data['data_start_work'],
                photo=form.cleaned_data['photo'],
                status='crt'
            )

            # # название задачи
            # t_name = f'Создать уз {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
            # # Описание задачи
            # t_description = f'Сотрудник {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]} ' \
            # f"дата рождения {form.cleaned_data['birth_date']}" \
            # f"отдел {form.cleaned_data['department']}"
            # f"должность {form.cleaned_data['position']}"

    else:
        form = ProfileForm()
    return render(request, 'worker/create_profile.html', {'form': form, 'section': 'task_add_profile'})


@login_required
def show_profiles(request):
    profiles = Profile.objects.filter(user__is_active=True)
    return render(
        request,
        template_name='worker/show_profiles.html',
        context={
            'profiles': profiles,
            'section': 'profiles'}
        )

