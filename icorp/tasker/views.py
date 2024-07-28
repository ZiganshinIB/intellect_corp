from django.shortcuts import render, get_object_or_404

from .forms import PasswordForm
from worker.models import Profile


def create_profile_list(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles,
               'section': 'crate_profile'}
    return render(
        request,
        template_name='tasker/create_profile_list.html',
        context=context)


def create_profile_detail(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {
        'profile': profile,
        'section': 'create_profile_detail'
    }
    return render(
        request,
        template_name='tasker/create_profile_detail.html',
        context=context)


def add_password(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    form = PasswordForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = request.POST
            print(cd)

    return render(
        request,
        template_name='tasker/create_password.html',
        context={
            'profile': profile,
            'form': form
        })
