from django.utils import timezone
from django.contrib.auth import get_user_model
from celery import shared_task
from datetime import timedelta
from .models import Report
from .serializers import ReportSerializer


User = get_user_model()


@shared_task
def generate_weekly_report():
    users = User.objects.all()
    reports = []
    for user in users:
        report = Report(user=user)

        report.starting_date = timezone.now().date() - timedelta(days=7)
        report.ending_date = timezone.now().date()

        report.save()

        user_completed_tasks = user.tasks.filter(
            completed_at__range=(report.starting_date, report.ending_date)
        )
        user_completed_projects = user.projects.filter(
            completed_at__range=(report.starting_date, report.ending_date)
        )

        for task in user_completed_tasks:
            task.report = report
            task.save()

        for project in user_completed_projects:
            project.report = report
            project.save()

        serializer = ReportSerializer(report)
        reports.append(serializer.data)

    return reports
