from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from task_management.models import Task
from task_management.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
