from rest_framework import serializers
from core.abstract.serializer import AbstractSerializer
from rest_framework.exceptions import ValidationError
from core.post.models import Post
from core.user.models import User
from core.comment.models import Comment
from core.user.serializers import UserSerializer
from core.post.serializers import PostSerializer



class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset= User.objects.all(), slug_field='public_id')
    post = serializers.SlugRelatedField(queryset= Post.objects.all(), slug_field='public_id') 


    def validate_author(self, value):
        
        if value != self.context['request'].user:
            raise ValidationError('you can only comment as yourself') 
        
        return value
    


    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        
        return value


    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        
        instance = super().update(instance, validated_data)
        return instance


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data 

        post = Post.objects.get_object_by_public_id(rep['post'])
        rep['post'] = PostSerializer(post).data


        return rep
    

    class Meta:
        model = Comment
        fields = ['id','author', 'post', 'body', 'edited', 'created', 'updated']
        read_only_fields = ['edited'] 