from rest_framework.permissions import BasePermission


class ProjectsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            if obj.title == "Tasks":
                return False
        return True
