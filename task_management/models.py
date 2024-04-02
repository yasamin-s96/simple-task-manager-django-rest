from django.db import models


# Create your models here.
class Task(models.Model):
    STATUS = [("pending", "Pending"), ("complete", "Complete")]
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Project(models.Model):
    name = models.CharField(max_length=100)

