from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import ReportSerializer


# Create your views here.
class ReportListView(ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        return self.request.user.reports
