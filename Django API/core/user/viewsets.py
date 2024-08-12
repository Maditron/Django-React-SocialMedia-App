from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from core.user.serializers import UserSerializer
from core.user.models import User
from core.abstract.viewsets import AbstractViewset
from rest_framework.parsers import MultiPartParser, FormParser


class UserViewset(AbstractViewset):
    http_method_names = ['patch', 'get']
    permission_classes = [IsAuthenticated] 
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser] 
    

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username:
            queryset = User.objects.filter(username=username)  
            return queryset
        
        if self.request.user.is_superuser:
            return User.objects.all() 
        return User.objects.exclude(is_superuser=True) 
    

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk']) 
        self.check_object_permissions(self.request, obj)
        return obj 

    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }