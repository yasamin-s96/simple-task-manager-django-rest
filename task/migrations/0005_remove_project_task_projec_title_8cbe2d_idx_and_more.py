# Generated by Django 5.0.3 on 2024-04-14 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0004_alter_task_project"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="project",
            name="task_projec_title_8cbe2d_idx",
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(
                fields=["user", "title"], name="task_projec_user_id_e444db_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tag",
            index=models.Index(
                fields=["user", "title"], name="task_tag_user_id_077b9a_idx"
            ),
        ),
    ]
