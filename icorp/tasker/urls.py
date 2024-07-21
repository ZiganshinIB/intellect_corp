from django.urls import path

from . import views

app_name = 'tasker'

urlpatterns = [
    path('create_profile/', views.create_profile_list, name='create_profile_list'),
    path('create_profile/<int:pk>/', views.create_profile_detail, name='create_profile_detail'),
]
