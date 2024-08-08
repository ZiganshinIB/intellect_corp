from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response


from worker.models import Profile

from .models import Task
from .serializers import TaskSerializer
from .forms import PasswordForm
from .permissions import IsOwnerOrAssignedOrReadOnly


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
    """
    Добавление пароля сотруднику профиля
    """
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


class TaskAPIList(ListCreateAPIView):
    """
    Создание задания через API
    """
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrAssignedOrReadOnly,)

    def get_queryset(self):
        return Task.objects.filter(Q(assigned_to=self.request.user) | Q(created_by=self.request.user))


