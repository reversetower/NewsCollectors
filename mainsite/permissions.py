from rest_framework import permissions

#���K��̵����v��, ��l�ȯ�Ū��
class IsPosterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.poster == request.user

#��managers�s�զ��v��
class IsManagers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="managers").exists()

#�Ȥw�n�J�ϥΪ̥��H���v��
class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user