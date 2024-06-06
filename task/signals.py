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


@receiver(pre_save, sender=Task)
def detect_recurring_task(sender, instance, **kwargs):
    try:
        original = sender.objects.get(id=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        repeat_schedule = instance.repeat_schedule or original.repeat_schedule
        if (
            repeat_schedule
            and instance.status != original.status
            and instance.status == "complete"
        ):

            due_date = instance.due_date or instance.due_date
            if not due_date:
                due_date = timezone.now().date()

            new_upcoming_task = Task(
                user=original.user,
                description=instance.description or original.description,
                priority=instance.priority or original.priority,
                side_note=instance.side_note or original.side_note,
                project=instance.project or original.project,
                report=None,
                repeat_schedule=repeat_schedule,
                due_date=due_date + repeat_schedule,
            )

            new_upcoming_task.save()

            new_upcoming_task.tags.set(instance.tags.all() or original.tags.all())
