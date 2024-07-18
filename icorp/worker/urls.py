from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('create_profile/', views.create_task_add_profile, name='create_profile'),

]

