from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    assumes the model instance has an 'owner' attribute
    """
    
    def has_object_permission(self,request,view,id):
        # Read permissions are allowed to any request,
        # so we'll always allow Get, Head or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author.user == request.user