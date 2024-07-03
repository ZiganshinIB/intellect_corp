# Generated by Django 4.2.9 on 2024-07-03 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Группа')),
                ('system', models.CharField(choices=[('AD', 'Active Directory'), ('B24', 'Bitrix24'), ('1C', '1C'), ('PSI', 'Openfire'), ('IC', 'Intellect_corp')], max_length=5, verbose_name='Система')),
                ('sname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Системное имя')),
                ('path', models.CharField(blank=True, max_length=512, null=True, verbose_name='Путь')),
            ],
            options={
                'verbose_name': 'Группа доступа',
                'verbose_name_plural': 'Группы доступа',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Компания')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес')),
                ('inn', models.CharField(blank=True, max_length=100, null=True, verbose_name='ИНН')),
                ('chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Должность')),
                ('department', models.CharField(max_length=100, verbose_name='Отдел')),
                ('permissions', models.ManyToManyField(blank=True, to='worker.accessgroup', verbose_name='Разрешения')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='static/img/default.jpg', upload_to='media/users/%Y/%m/%d/', verbose_name='Фото')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('internal_phone', models.CharField(blank=True, max_length=3, null=True, verbose_name='Внутренний телефон')),
                ('chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель')),
                ('permissions', models.ManyToManyField(blank=True, related_name='permissions', to='worker.accessgroup', verbose_name='Разрешения')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worker.position', verbose_name='Должность')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Отдел')),
                ('chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.company', verbose_name='Компания')),
            ],
        ),
    ]