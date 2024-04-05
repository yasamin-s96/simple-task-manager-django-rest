from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import timedelta
from .models import Task
from .serializers import TaskSerializer, SimpleTaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    @action(detail=False, methods=["get", "post"])
    def today(self, request):
        """
        Displaying the tasks due till the end of the current day.
        """

        if request.method == "GET":
            queryset = self.get_queryset()
            today_tasks = queryset.filter(due_date__lt=timezone.now().date() + timedelta(days=1))
            serializer = SimpleTaskSerializer(today_tasks, many=True)
            return Response(serializer.data)

        else:
            serializer_context = self.get_serializer_context()
            serializer_context["today"] = True
            serializer = SimpleTaskSerializer(data=request.data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return SimpleTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        """
        List view should return a list of all the tasks created by the authenticated user.
        """
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.request.user.id
        return context


class TodayViewSet(ModelViewSet):
    serializer_class = SimpleTaskSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return Task.objects.incomplete_tasks() \
            .prefetch_related("tags").select_related("project") \
            .filter(user=self.request.user, due_date__lt=timezone.now().date() + timedelta(days=1))
