from django.utils import timezone
from rest_framework import serializers
from datetime import timedelta
from .models import Task, Project, Tag


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
        data["tags"] = [tag.title for tag in instance.tags.all()]
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
            if Project.objects.filter(id=project_id).exists():
                validated_data["project_id"] = project_id
            else:
                raise serializers.ValidationError({"project": f"Project with ID {project_id} does not exist."})

        if self.context.get("today"):
            validated_data["due_date"] = timezone.now()

        elif self.context.get("tomorrow"):
            validated_data["due_date"] = timezone.now() + timedelta(days=1)

        validated_data["user_id"] = self.context["user_id"]

        task = super().create(validated_data)
        if tag_id := self.context.get("tag_id"):
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError({"tags": f"Tag with ID {tag_id} does not exist."})
            else:
                task.tags.add(tag)
        return task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "status"]

    def validate_title(self, value):
        if Project.objects.filter(user_id=self.context["user_id"], title=value).exists():
            raise serializers.ValidationError({"title": "A project with the given title already exists."})
        return value


class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title"]

    def validate_title(self, value):
        if Tag.objects.filter(user_id=self.context["user_id"], title=value).exists():
            raise serializers.ValidationError({"title": "A tag with the given title already exists."})
        return value
