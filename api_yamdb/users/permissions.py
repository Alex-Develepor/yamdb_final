from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Редактирование возможно только для Администратора.
    Для чтения доступно всем.
    """
    message = 'Не хватает прав для редактирования, нужны права Администратора'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Редактирование возможно только автора, администратора/модератора.
    Для чтения доступно всем.
    """
    message = 'Редактировать можно только свои отзывы, либо админ/модератор'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and (
                    request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                ))


class UserIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class UserIsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UserIsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator
