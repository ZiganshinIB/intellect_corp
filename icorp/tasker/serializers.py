
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'created_by', 'assigned_to', 'created_at', 'updated_at')
