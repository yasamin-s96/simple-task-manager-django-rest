from django.db import models
from django.conf import settings

# Create your models here.


class Report(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    starting_date = models.DateField()
    ending_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-created_at"])]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s report from {self.starting_date} to {self.ending_date}"
