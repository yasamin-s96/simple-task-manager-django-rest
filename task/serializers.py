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

    def create(self, validated_data):
        if self.context.get("today"):
            validated_data["due_date"] = timezone.now()
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



