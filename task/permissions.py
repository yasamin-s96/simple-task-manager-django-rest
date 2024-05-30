from rest_framework.permissions import BasePermission


class ProjectsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.title == "Tasks":
            if request.method == "DELETE":
                return False
            elif request.method in ["PUT", "PATCH"]:
                status = request.data.get("status")
                if status and status == "complete":
                    return False
        return True
