from django.db import models


class TaskManager(models.Manager):
    def incomplete_tasks(self):
        return self.filter(status="pending")
