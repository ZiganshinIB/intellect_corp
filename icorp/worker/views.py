from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from tasker.models import Task
from .models import Profile
from .forms import ProfileForm


def index(request):
    return render(request, 'worker/index.html')


def create_task_add_profile(request):
    """ Create task and add profile to it """
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Необходимо создать задачу и добавить данные профиля
            # название задачи
            t_name = f'Создать уз {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
            # Описание задачи
            t_description = f'Сотрудник {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]} ' \
            f"дата рождения {form.cleaned_data['birth_date']}" \
            f"отдел {form.cleaned_data['department']}"
            f"должность {form.cleaned_data['position']}"

    else:
        form = ProfileForm()
    return render(request, 'worker/create_profile.html', {'form': form, 'section': 'create_profile'})

