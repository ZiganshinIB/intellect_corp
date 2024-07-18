from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskerAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status']






