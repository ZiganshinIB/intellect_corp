from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    profile = request.user.profile
    context = {
        'profile': profile,
        'section': 'dashboard'
    }
    return render(request,
                  'account/dashboard.html',
                  context=context)
