from core.abstract.serializer import AbstractSerializer
from core.post.models import Post
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.user.models import User
from core.user.serializers import UserSerializer



class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')  


    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField() 


    def get_comments_count(self, instance):
        return instance.comments.count() 


    def get_liked(self, instance):
        request = self.context.get('request')
        
        if request is None or request.user.is_anonymous:
            return False
    
    
        return request.user.has_liked(instance) 
    

    def get_likes_count(self, instance):
        return instance.likes.count()



    def validate_author(self, value):
        user = self.context['request'].user
        # if not user.is_authenticated:
        #     raise serializers.ValidationError('you must be logged in to create a post') this is taken care of in permissions
        
        if user != value:
            raise ValidationError('you cannot create a post for another user')
        
        return value
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited','created', 'updated', 'liked', 'likes_count', 'comments_count']   
        read_only_fields = ["edited"] 


    def to_representation(self, instance):
        rep = super().to_representation(instance) 

        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data 

        return rep 
    

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        instance = super().update(instance, validated_data)
        return instance
    
