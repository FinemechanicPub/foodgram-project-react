from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object level permission that allows access for writing to
    object author
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user == obj.author
        ) or request.method in permissions.SAFE_METHODS
