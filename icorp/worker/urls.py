from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
]

