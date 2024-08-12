from django.test import TestCase
import pytest
from core.user.models import User
from core.post.models import Post




data_user = {
    'username': "test_user",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password"
}


data_superuser = {
"username": "test_superuser",
"email": "testsuperuser@example.com",
"first_name": "Test",
"last_name": "Superuser",
"password": "test_password"
}



@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(**data_user)
    assert user.username == data_user['username']
    assert user.email == data_user['email']
    assert user.first_name == data_user['first_name']
    assert user.last_name == data_user['last_name']
    # assert user.password == data_user['password']



@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(**data_superuser)
    assert user.username == data_superuser["username"]
    assert user.email == data_superuser["email"]
    assert user.first_name == data_superuser["first_name"]
    assert user.last_name == data_superuser["last_name"]
    assert user.is_superuser == True
    assert user.is_staff == True


@pytest.mark.django_db
def test_like_db():
    user = User.objects.create_user(**data_user)
    post = Post.objects.create(author=user, body='test post')
    post2 = Post.objects.create(author=user, body='test post 2')
    
    assert not user.posts_liked.exists()
    assert not user.has_liked(post)
    
    user.like(post)
    user.refresh_from_db() 

    assert post in user.posts_liked.all() 
    assert user.posts_liked.count() == 1
    assert user.has_liked(post) 
    assert not user.has_liked(post2) 

    user.remove_like(post)
    user.refresh_from_db()

    assert not post in user.posts_liked.all() 
    assert user.posts_liked.count() == 0
