from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from datetime import timedelta
from .models import Task, Project, Tag
from .serializers import TaskSerializer, SimpleTaskSerializer, SimpleProjectSerializer, ProjectSerializer, TagSerializer


class TaskViewSet(ModelViewSet):
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project", "due_date"]

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return SimpleTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class TodayViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = SimpleTaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project", "due_date"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__lt=timezone.now().date() + timedelta(days=1))

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "today": True}


class TomorrowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = SimpleTaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__date=timezone.now().date() + timedelta(days=1))

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "tomorrow": True}


class PlannedViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = SimpleTaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project", "due_date"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__isnull=False)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "today": True}


class ProjectViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return SimpleProjectSerializer
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user, status="pending")
        # pending_tasks = Task.objects.incomplete_tasks().prefetch_related("tags")
        # prefetch = Prefetch("tasks", pending_tasks)
        # return Project.objects.prefetch_related(prefetch) \
        #     .filter(user=self.request.user, status="pending")

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class ProjectRelatedTaskViewSet(TaskViewSet):

    def get_queryset(self):
        return Task.objects.incomplete_tasks().prefetch_related("tags") \
            .select_related("project").filter(project_id=self.kwargs["project_pk"])

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "project_id": self.kwargs["project_pk"]}


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class TagRelatedTaskViewSet(TaskViewSet):
    def get_queryset(self):
        return Task.objects.incomplete_tasks().prefetch_related("tags") \
            .select_related("project").filter(tags=self.kwargs["tag_pk"])

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "tag_id": self.kwargs["tag_pk"]}


class CompletedTaskViewSet(ModelViewSet):
    http_method_names = ["get", "put", "patch", "delete"]

    def get_queryset(self):
        return Task.objects.prefetch_related("tags") \
            .select_related("project").filter(user=self.request.user, status="complete")
