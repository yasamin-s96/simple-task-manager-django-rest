from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("tasks", views.TaskViewSet, basename="task")
router.register("today", views.TodayViewSet, basename="today")
router.register("tomorrow", views.TomorrowViewSet, basename="tomorrow")
router.register("planned", views.PlannedViewSet, basename="planned")
router.register("projects", views.ProjectViewSet, basename="project")
project_router = routers.NestedDefaultRouter(router, "projects", lookup="project")
project_router.register("tasks", views.ProjectRelatedTaskViewSet, basename="task")
urlpatterns = router.urls + project_router.urls
