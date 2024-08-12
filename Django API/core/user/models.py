from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404 
from core.abstract.models import AbstractManager, AbstractModel
from core.post.models import Post
from django.conf import settings



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.public_id, filename) 


class UserManager(BaseUserManager, AbstractManager):
        
    
    def create_user(self,username, email, password=None, **kwargs):
        if not username:
            raise TypeError('user must have a username')
        if not email:
            raise TypeError('user must have an email')
        if not password:
            raise TypeError('user must have a password')
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) 

        return user




class User(AbstractBaseUser, PermissionsMixin, AbstractModel):

    username = models.CharField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    posts_liked = models.ManyToManyField(Post, related_name='likes') 
    bio = models.CharField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')      

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] 

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}"
    
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    

    def like(self, post):
        self.posts_liked.add(post) 


    def remove_like(self, post):
        self.posts_liked.remove(post)

    
    def has_liked(self, post):
        return self.posts_liked.filter(pk=post.pk).exists() 




    