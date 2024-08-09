from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # import pdb; pdb.set_trace()
        
        print(request.user)
        return request.user and request.user.is_authenticated
    

class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request)
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request)
        return request.user and request.user.is_staff


class IsAdminOrIsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdmin().has_permission(request, view) or IsCreator().has_object_permission(request, view, obj)
