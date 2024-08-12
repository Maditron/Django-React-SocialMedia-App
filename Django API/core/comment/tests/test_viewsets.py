from core.fixtures.user import user, user2
from core.fixtures.post import post
from conftest import client
import pytest
from rest_framework import status
from core.fixtures.comment import comment



class TestCommentViewset:

    endpoint = '/api/v1/post/'


    def test_list(self, client, user, post, comment):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + '/comment/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    

    def test_retrieve(self, client, user, post, comment):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == comment.public_id.hex
        assert response.data['author']['id'] == comment.author.public_id.hex
        assert response.data['post']['id'] == comment.post.public_id.hex
        assert response.data['body'] == comment.body

    
    def test_create(self, client, user, user2, post):
        client.force_authenticate(user=user2)
        data= {
            'author': user2.public_id.hex,
            'post': post.public_id.hex,
            'body': "test comment body"
        }

        response = client.post(self.endpoint + str(post.public_id) + '/comment/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author']['id'] == user2.public_id.hex
        assert response.data['post']['id'] == post.public_id.hex
        assert response.data['body'] == data['body']
    


    def test_update(self, client, user, post, comment):
        client.force_authenticate(user=user)
        data= {
            'author': user.public_id.hex,
            'post': post.public_id.hex,
            'body': "test comment body"
        }

        response = client.put(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['author']['id'] == data['author']
        assert response.data['body'] == data['body']
        assert response.data['id'] == comment.public_id.hex
        assert response.data['post']['id'] == data['post'] 




    def test_update_another_user(self, client, user2, post, comment):
        client.force_authenticate(user=user2)
        data= {
            'author': user2.public_id.hex,
            'post': post.public_id.hex,
            'body': "test comment body"
        }

        # this comment is for user1. So user2 should not be able to update it. 

        response = client.put(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/', data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


    
    def test_delete(self, client, user, post, comment):
        client.force_authenticate(user= user)

        response = client.delete(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')
        assert response.status_code == status.HTTP_204_NO_CONTENT



    
    def test_delete_another_user(self, client, user2, post, comment):
        client.force_authenticate(user= user2)

        response = client.delete(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


    
    def test_list_anonymous(self, client, post, comment):
        response = client.get(self.endpoint + str(post.public_id) + '/comment/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    

    def test_retrieve_anonymous(self, client, post, comment):
        response = client.get(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == comment.public_id.hex
        assert response.data['author']['id'] == comment.author.public_id.hex
        assert response.data['post']['id'] == post.public_id.hex
        assert response.data['body'] == comment.body
    

    def test_create_anonymous(self, client, post):
        data= {
            'author': 'test_user',
            'post': post.public_id.hex,
            'body': "test comment body"
        }

        response = client.post(self.endpoint + str(post.public_id) + '/comment/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    



    def test_update_anonymous(self, client, post, comment):
        data= {
            'author': 'test_user',
            'post': post.public_id.hex,
            'body': "test comment body"
        }

        response = client.put(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    


    def test_delete_anonymous(self, client, post, comment):
        response = client.delete(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 