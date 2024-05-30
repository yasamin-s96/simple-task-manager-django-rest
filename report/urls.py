from django.urls import path
from . import views


urlpatterns = [path("weekly-reports/", views.ReportListView.as_view())]
