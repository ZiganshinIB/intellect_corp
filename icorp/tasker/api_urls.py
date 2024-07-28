from django.urls import path, include
from . import views

urlpatterns = [
    path('api/tasks/', views.TaskAPIList.as_view(), name='task_list_create'),
]