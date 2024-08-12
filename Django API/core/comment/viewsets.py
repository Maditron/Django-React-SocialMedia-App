from core.abstract.viewsets import AbstractViewset
from rest_framework.response import Response
from django.http.response import Http404
from rest_framework import status
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.post.permissions import IsAuthorOrReadOnly, IsAuthorOrReadOnly2



class CommentViewset(AbstractViewset):
    http_method_names =['get', 'post','put','delete']
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly2]


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        
        post_pk = self.kwargs['post_pk']
        if not post_pk:
            return Http404
        
        queryset = Comment.objects.filter(post__public_id = post_pk)

        return queryset
    

    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj
    


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)