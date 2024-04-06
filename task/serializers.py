from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=Task.PRIORITY, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "project",
            "tags",
            "status",
            "side_note",
            "due_date",
        ]

    def to_representation(self, instance):
        # Serializing project field with its title instead of ID.
        data = super().to_representation(instance)
        data["project"] = instance.project.title if instance.project else None
        return data

    def create(self, validated_data):
        if self.context.get("today"):
            validated_data["due_date"] = timezone.now()
        elif self.context.get("tomorrow"):
            validated_data["due_date"] = timezone.now() + timedelta(days=1)
        validated_data["user_id"] = self.context["user_id"]
        return super().create(validated_data)


class SimpleTaskSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "project",
            "tags",
            "due_date",
        ]
