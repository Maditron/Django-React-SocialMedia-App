from core.user.models import User
from rest_framework import serializers
from core.abstract.serializer import AbstractSerializer
from django.conf import settings
import random


class UserSerializer(AbstractSerializer):

    name = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
        

    def get_posts_count(self, obj):
        return obj.posts.count() 

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'avatar', 'bio', 'first_name',
                  'last_name', 'email', 'is_superuser', 'is_active', 'created', 'updated', 'posts_count']
        read_only_fields = ['is_active']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not rep['avatar']:
            rep['avatar'] = settings.DEFAULT_AVATAR_PATH
       
        elif 'http' not in rep['avatar']:
            rep['avatar'] = 'http://localhost:8000/' + rep['avatar'].lstrip('/')
            rep['avatar'] = rep['avatar'].lstrip('/')   
        

        
        return rep