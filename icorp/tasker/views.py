from django.shortcuts import render

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
