from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class OwnerAndAdminChange(IsAuthenticatedOrReadOnly):
    """Permission for owner or Admin."""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_staff)

