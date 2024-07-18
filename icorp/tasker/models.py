from django.db import models


class TaskStatus(models.Model):
    """ Статус """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


# Задачи
class Task(models.Model):
    """ Задача """
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                    related_name='assigned_tasks',
                                    null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Approval(models.Model):
    STATUS = (
        ('pen', 'Ожидает согласования'),
        ('apr', 'Согласовано'),
        ('rej', 'Отклонено'),
    )

    """ Согласование """
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                    related_name='assigned_approvals',
                                    null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Согласование'
        verbose_name_plural = 'Согласования'



