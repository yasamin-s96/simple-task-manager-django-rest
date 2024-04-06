from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("today", views.TodayViewSet, basename="today")
router.register("tomorrow", views.TomorrowViewSet, basename="tomorrow")
router.register("", views.TaskViewSet, basename="task")  # basename plural or singular?

urlpatterns = router.urls
