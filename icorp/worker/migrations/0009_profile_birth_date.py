# Generated by Django 4.2.9 on 2024-07-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0008_profile_patronymic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]