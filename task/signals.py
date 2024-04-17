from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Task


@receiver(pre_save, sender=Task)
def detect_task_completion(sender, instance, **kwargs):
    try:
        original = sender.objects.get(id=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if instance.status != original.status and instance.status == "complete":
            instance.completed_at = timezone.now().date()
