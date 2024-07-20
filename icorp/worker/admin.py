from django.contrib import admin

from .models import Company, Department, Position, Profile, AccessGroup


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'inn', 'chief']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'chief']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'department',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'position_department', 'chief']

    def position_department(self, obj):
        if not obj.position:
            return ''
        return obj.position.department
    position_department.short_description = 'Отдел'


@admin.register(AccessGroup)
class AccessGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


