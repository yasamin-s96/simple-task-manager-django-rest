from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=Task.PRIORITY, allow_null=True)

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
        """
        Removing "" from tha validated data in order to get it populated with the default value set by the model.
        """
        if not validated_data["priority"]:
            validated_data.pop("priority")
        return super().create(validated_data)


class UpdateTaskSerializer(TaskSerializer):
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


class DetailedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "project",
            "tags",
            "side_note",
            "due_date",
        ]
