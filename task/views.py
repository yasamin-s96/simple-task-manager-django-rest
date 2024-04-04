from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import timedelta
from .models import Task
from .serializers import TaskSerializer, UpdateTaskSerializer, DetailedTaskSerializer


class TaskViewSet(ModelViewSet):

    @action(detail=False)
    def today(self, request):
        """
        Displaying the tasks due till the end of the current day.
        """
        queryset = self.get_queryset()
        today_tasks = queryset.filter(due_date__lt=timezone.now().date() + timedelta(days=1))
        serializer = TaskSerializer(today_tasks, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "update":
            return UpdateTaskSerializer
        elif self.action == "retrieve":
            return DetailedTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        """
        This view should return a list of all the tasks created by the authenticated user.
        """
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Overriding to pass user to the serializer.
        """
        serializer.save(user=self.request.user)
