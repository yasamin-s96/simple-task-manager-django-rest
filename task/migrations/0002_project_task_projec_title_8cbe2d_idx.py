# Generated by Django 5.0.3 on 2024-04-07 06:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="project",
            index=models.Index(fields=["title"], name="task_projec_title_8cbe2d_idx"),
        ),
    ]
