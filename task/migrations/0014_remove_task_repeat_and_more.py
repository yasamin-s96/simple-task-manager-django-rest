# Generated by Django 5.0.3 on 2024-06-06 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0013_alter_task_created_at_alter_task_due_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="repeat",
        ),
        migrations.RemoveField(
            model_name="task",
            name="repeat_schedule_start_date",
        ),
    ]
