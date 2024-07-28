from django.urls import path, include

from . import views

app_name = 'tasker'

urlpatterns = [
    path('', include('tasker.api_urls')),
    path('create_profile/', views.create_profile_list, name='create_profile_list'),
    path('create_profile/<int:pk>/', views.create_profile_detail, name='create_profile_detail'),
    path('create_password/<int:pk>/', views.add_password, name='create_password'),

]
