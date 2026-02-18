from rest_framework import permissions


class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Librarians can edit.
    Members can only read.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
    

class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET']=['%(app_label)s.view_%(model_name)s']
        
        
class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        return obj.user == request.user