from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.conf import settings

from PIL import Image
from phonenumber_field import modelfields

# form . import ...

UserModel = settings.AUTH_USER_MODEL


class AccessGroup(models.Model):
    SYSTEMS = (
        ('AD', 'Active Directory'),
        ('B24', 'Bitrix24'),
        ('1C', '1C'),
        # ('SAP', 'SAP'),
        ('PSI', 'Openfire'),
        ('IC', 'Intellect_corp'),
    )
    name = models.CharField(max_length=100,
                            verbose_name="Группа")
    system = models.CharField(max_length=5,
                              verbose_name="Система",
                              choices=SYSTEMS)
    sname = models.CharField(max_length=100,
                             verbose_name="Системное имя",
                             blank=True,
                             null=True)
    path = models.CharField(max_length=512,
                            verbose_name="Путь",
                            blank=True,
                            null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа доступа"
        verbose_name_plural = "Группы доступа"


class Company(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Компания")
    address = models.CharField(max_length=100,
                               verbose_name="Адрес",
                               blank=True,
                               null=True)
    inn = models.CharField(max_length=100,
                            verbose_name="ИНН",
                           blank=True,
                           null=True)
    # Директор компании
    chief = models.ForeignKey(UserModel,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name="companies",
                              verbose_name="Руководитель")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Department(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Отдел")

    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                verbose_name="Компания")
    chief = models.ForeignKey(UserModel,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name="departments",
                              verbose_name="Руководитель")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"


class Position(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Должность")
    department = models.ForeignKey(Department,
                                   on_delete=models.CASCADE,
                                   related_name="positions",
                                   verbose_name="Отдел")
    path_ou = models.CharField(max_length=512, verbose_name="OU", blank=True, null=True)
    permissions = models.ManyToManyField("AccessGroup",
                                         blank=True,
                                         verbose_name="Разрешения")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return "{} - {}".format(self.name, self.department)


class Profile(models.Model):
    STATUS = (
        ('crt', 'Запрошен'),
        ('act', 'Активен'),
        ('blk', 'Блокирован'),
    )
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                related_name="profile",
                                verbose_name="Пользователь")
    # отчество
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")

    photo = models.ImageField(upload_to="media/users/%Y/%m/%d/",
                              verbose_name="Фото",
                              default="media/profile_default.jpg",
                              )
    phone = modelfields.PhoneNumberField(blank=True, null=True,
                                         verbose_name="Телефон")
    internal_phone = models.CharField(max_length=3,
                                      blank=True,
                                      null=True,
                                      verbose_name="Внутренний телефон")
    position = models.ForeignKey(Position,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name="Должность")
    permissions = models.ManyToManyField("AccessGroup",
                                         blank=True,
                                         related_name="permissions",
                                         verbose_name="Разрешения")
    data_start_work = models.DateField(blank=True,
                                       null=True,
                                       verbose_name="Дата начала работы")
    chief = models.ForeignKey(UserModel,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name="profiles",
                              verbose_name="Руководитель")
    status = models.CharField(max_length=3, choices=STATUS, default='crt', verbose_name="Статус")

    def full_name(self):
        return self.user.first_name + " " + self.user.last_name  + f" {self.patronymic}" if self.patronymic else ""

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)

    def save(
        self, *args, **kwargs
    ):
        super().save(*args, **kwargs)
        img = Image.open(self.photo)
        if img.height > 180 or img.width > 180:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


# При создании пользователя создаем профиль
@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# При изменении поля группы доступа обновляем их профилей
@receiver(post_save, sender=Position)
def update_position(sender, instance, created, **kwargs):
    profiles = Profile.objects.filter(position=instance)
    for profile in profiles:
        for permission in instance.permissions.all():
            if permission not in profile.permissions.all():
                profile.permissions.add(permission)

