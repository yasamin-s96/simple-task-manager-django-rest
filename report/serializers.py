from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)
    projects = serializers.StringRelatedField(many=True)

    class Meta:
        model = Report
        fields = ["tasks", "projects", "starting_date", "ending_date"]
