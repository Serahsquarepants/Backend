# from rest_framework import permissions

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    admin_methods = ['POST','PUT','PATCH','DELETE']
    
    def has_permission(self, request, view):
        if request.method in self.admin_methods:
            return request.user.is_staff  
        return True 