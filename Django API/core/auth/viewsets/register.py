from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.auth.serializers.register import RegisterSerializer



class RegisterViewset(ViewSet):
    http_method_names = ['post']
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(
            {
                'user': serializer.data,
                'access': res['access'],
                'refresh': res['refresh'],
            },
            status= status.HTTP_201_CREATED
        ) 