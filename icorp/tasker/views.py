from django.shortcuts import render


def create_profile_list(request):
    return render(request, 'tasker/create_profile_list.html')
