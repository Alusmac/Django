from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Custom permission that allows read-only access for any user,
    but write access only for admin users
    """

    def has_permission(self, request, view) -> bool:
        """Check if the request has permission
        """

        if request.method in ["GET"]:
            return True

        return request.user and request.user.is_staff
