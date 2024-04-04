from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.TaskViewSet, basename="task")  # basename plural or singular?

urlpatterns = router.urls
