from rest_framework import permissions


class IsAuthorOrAuthenticatedOrReadOnlyPermission(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit
    or delete it. Assumes the model instance has an `author` attribute.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        # Instance must have an attribute named `author`.
        return obj.author == request.user
