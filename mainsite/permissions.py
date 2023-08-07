from rest_framework import permissions

#除貼文者給予權限, 其餘僅能讀取
class IsPosterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.poster == request.user

#僅managers群組有權限
class IsManagers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="managers").exists()

#僅已登入使用者本人有權限
class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user