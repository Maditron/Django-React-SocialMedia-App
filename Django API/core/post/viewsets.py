from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from core.abstract.viewsets import AbstractViewset
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from core.user.models import User
from core.user.serializers import UserSerializer
from rest_framework.decorators import action



class PostViewset(AbstractViewset):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly] 


    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author__public_id', None)
        if author_id:
            queryset = queryset.filter(author__public_id=author_id) 
        return queryset



    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk']) 

        self.check_object_permissions(self.request, obj)

        return obj
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    

    @action(methods=['post'], detail=True) 
    def like(self, *args, **kwargs):
        post = self.get_object() 
        user = self.request.user

        user.like(post) 
        
        serializer = self.serializer_class(post, context={'request': self.request})     
         

        return Response(serializer.data, status=status.HTTP_200_OK)  
    # Like a post with the following endpoint: api/post/post_pk/like/


    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object() 
        user = self.request.user

        user.remove_like(post)
        
        serializer = self.serializer_class(post) 

        return Response(serializer.data, status=status.HTTP_200_OK)  
    # Like a post with the following endpoint: api/post/post_pk/remove_like/