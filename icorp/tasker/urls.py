from django.urls import path

from . import views

app_name = 'tasker'

urlpatterns = [
    path('create_profile/', views.create_profile_list, name='create_profile_list'),
]
