from rest_framework import routers
from core.user.viewsets import UserViewset
from core.auth.viewsets.register import RegisterViewset
from core.auth.viewsets.login import LoginViewset
from core.auth.viewsets.refresh import RefreshViewset
from core.post.viewsets import PostViewset
from rest_framework_nested import routers
from core.comment.viewsets import CommentViewset
from django.conf import settings
from django.conf.urls.static import static



router = routers.SimpleRouter()

router.register(r'user', UserViewset, basename='user')
router.register(r'auth/register', RegisterViewset, basename='auth-register') 
router.register(r'auth/login', LoginViewset, basename='auth-login') 
router.register(r'auth/refresh', RefreshViewset, basename='auth-refresh') 
router.register(r'post', PostViewset, basename='post')


post_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
post_router.register(r'comment', CommentViewset, basename='post-comment')




urlpatterns = [
    *router.urls,
    *post_router.urls
]