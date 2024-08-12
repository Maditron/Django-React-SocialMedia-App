from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
    
        return (request.user and request.user.is_authenticated) 


    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if request.method in ['DELETE', 'PUT']: 
            return (request.user.is_superuser or request.user in [obj.author]) 

        return (request.user and request.user.is_authenticated)  



class IsAuthorOrReadOnly2(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
    
        return (request.user and request.user.is_authenticated) 


    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if request.method in ['DELETE', 'PUT']:
            return (request.user.is_superuser or request.user in [obj.author, obj.post.author]) 

        return (request.user and request.user.is_authenticated)  
