from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import Profile
from .forms import ProfileForm


def index(request):
    return render(request, 'worker/index.html')


class CreateProfileView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'worker/create_profile.html'

