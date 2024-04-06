from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from datetime import timedelta
from .models import Task
from .serializers import TaskSerializer, SimpleTaskSerializer


class TaskViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return SimpleTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.request.user.id
        return context


class TodayViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = SimpleTaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project", "due_date"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__lt=timezone.now().date() + timedelta(days=1))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["today"] = True
        context["user_id"] = self.request.user.id
        return context


class TomorrowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = SimpleTaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority", "project"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__date=timezone.now().date() + timedelta(days=1))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["tomorrow"] = True
        context["user_id"] = self.request.user.id
        return context
