# Generated by Django 5.0.3 on 2024-06-02 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0012_task_repeat_task_repeat_schedule_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
