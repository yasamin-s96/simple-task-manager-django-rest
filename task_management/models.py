from django.db import models
from django.conf import settings

STATUS = [("pending", "Pending"), ("complete", "Complete")]


class Task(models.Model):
    PRIORITY = [(1, "High"), (2, "Medium"), (3, "Low"), (4, "None")]

    description = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY, default=4)
    side_note = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    tags = models.ManyToManyField("Tag")
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["priority"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-due_date"])
        ]

    def __str__(self):
        return self.description


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "title")]

    def __str__(self):
        return self.title


class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = [("user", "title")]

    def __str__(self):
        return self.title
