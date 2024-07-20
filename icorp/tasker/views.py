from django.shortcuts import render

from worker.models import Profile

def create_profile_list(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles,
               'section': 'create_profile'}
    return render(
        request,
        template_name='tasker/create_profile_list.html',
        context=context)
