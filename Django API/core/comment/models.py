from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from core.user.models import User
from core.post.models import Post
# Create your models here.



class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return self.author.name 