from django.utils import timezone
from rest_framework import serializers
from datetime import timedelta
from .models import Task, Project, Tag


class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=Task.PRIORITY, required=False)
    project = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

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


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user_id = self.context.get("user_id")
        queryset = super().get_queryset()
        if user_id:
            return queryset.filter(user__id=user_id)
        return queryset


class CreateTaskSerializer(serializers.ModelSerializer):
    project = UserFilteredPrimaryKeyRelatedField(
        queryset=Project.objects, required=False, allow_null=True
    )

    tags = UserFilteredPrimaryKeyRelatedField(
        many=True, queryset=Tag.objects, required=False
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "project",
            "tags",
            "repeat_schedule",
            "due_date",
        ]

    def create(self, validated_data):
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
                raise serializers.ValidationError(
                    {"tags": f"Tag with ID {tag_id} does not exist."}
                )
            else:
                task.tags.add(tag)
        return task


class UpdateTaskSerializer(CreateTaskSerializer):
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
            "repeat_schedule",
            "due_date",
        ]

    def update(self, instance, validated_data):
        if received_status := validated_data.get("status"):
            if instance.status == "pending" and received_status == "complete":
                instance.completed_at = timezone.now().date()
            elif instance.status == "complete" and received_status == "pending":
                instance.completed_at = None
        return super().update(instance, validated_data)


class SimpleTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        fields = [
            "id",
            "description",
            "priority",
            "project",
            "tags",
            "side_note",
            "due_date",
        ]


class CompletedTaskSerializer(TaskSerializer):
    completed_at = serializers.DateField(read_only=True)

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
            "completed_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "status"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title"]

    def validate_title(self, value):
        if Project.objects.filter(
            user_id=self.context["user_id"], title=value
        ).exists():
            raise serializers.ValidationError(
                {"title": "A project with the given title already exists."}
            )
        return value

    def create(self, validated_data):
        validated_data["user_id"] = self.context["user_id"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if received_status := validated_data.get("status"):
            if instance.status == "pending" and received_status == "complete":
                instance.completed_at = timezone.now().date()
            elif instance.status == "complete" and received_status == "pending":
                instance.completed_at = None
        return super().update(instance, validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title"]

    def validate_title(self, value):
        if Tag.objects.filter(user_id=self.context["user_id"], title=value).exists():
            raise serializers.ValidationError(
                {"title": "A tag with the given title already exists."}
            )
        return value

    def create(self, validated_data):
        validated_data["user_id"] = self.context["user_id"]
        return super().create(validated_data)
