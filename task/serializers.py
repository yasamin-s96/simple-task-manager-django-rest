from django.utils import timezone
from rest_framework import serializers
from datetime import timedelta
from .models import Task, Project


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

    def create(self, validated_data):
        if project_id := self.context.get("project_id"):
            validated_data["project_id"] = project_id
        if self.context.get("today"):
            validated_data["due_date"] = timezone.now()
        elif self.context.get("tomorrow"):
            validated_data["due_date"] = timezone.now() + timedelta(days=1)
        validated_data["user_id"] = self.context["user_id"]
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "status"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title"]
