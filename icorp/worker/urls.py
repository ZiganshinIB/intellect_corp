from django.urls import path
from . import views



urlpatterns = [
    # path('', views.index, name='dashboard'),
    path('profiles/', views.show_profiles, name="profiles"),
    path('create_profile/', views.create_task_add_profile, name='task_add_profile'),
]

