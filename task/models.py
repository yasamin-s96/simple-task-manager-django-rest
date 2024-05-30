from django.db import models
from django.conf import settings
from .managers import TaskManager
from report.models import Report

STATUS = [("pending", "Pending"), ("complete", "Complete")]


class Task(models.Model):
    PRIORITY = [(1, "High"), (2, "Medium"), (3, "Low"), (4, "None")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    report = models.ForeignKey(
        Report,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )
    description = models.CharField(max_length=255)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=4)
    side_note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    project = models.ForeignKey(
        "Project", on_delete=models.PROTECT, blank=True, null=True, related_name="tasks"
    )
    tags = models.ManyToManyField("Tag", blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateField(null=True, blank=True)

    objects = TaskManager()

    class Meta:
        indexes = [
            models.Index(fields=["priority"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-due_date"]),
        ]

    def __str__(self):
        return self.description

    def save(self, **kwargs):
        if not self.project:
            self.project, _ = Project.objects.get_or_create(
                title="Tasks", user=self.user
            )
        return super().save(**kwargs)


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    report = models.ForeignKey(
        Report,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = [("user", "title")]
        indexes = [models.Index(fields=["status"])]

    def __str__(self):
        return self.title


class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = [("user", "title")]

    def __str__(self):
        return self.title
