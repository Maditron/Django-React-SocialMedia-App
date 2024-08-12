from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.auth.serializers.register import RegisterSerializer
from core.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.utils import timezone



class LoginSerializer(TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 

    def validate(self, attrs): 
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = RegisterSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token) 

        if self.user:
            self.user.last_login = timezone.now()
            self.user.save() 
        
        return data


