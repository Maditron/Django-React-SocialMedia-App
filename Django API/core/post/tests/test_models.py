from django.test import TestCase
from core.post.models import Post
import pytest
from core.fixtures.user import user



@pytest.mark.django_db
def test_create_post(user):
    post = Post.objects.create(author=user, body='test post body')
    assert post.author == user
    assert post.body == 'test post body'