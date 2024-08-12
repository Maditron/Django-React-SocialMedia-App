from core.fixtures.post import post
from core.fixtures.user import user
from conftest import client
import pytest
from rest_framework import status



class TestPostViewset:

    endpoint = '/api/v1/post/'


    def test_list(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    
    def test_retrieve(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + '/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex

    
    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            'author': user.public_id.hex,
            "body": 'test post body'
        }

        response = client.post(self.endpoint, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author']['id'] == user.public_id.hex
        assert response.data['body'] == data['body']

    
    def test_update(self, client, user, post):
        client.force_authenticate(user=user)
        data = {
            "author": user.public_id.hex,
            "body": "test post body edited"
        }

        response = client.put(self.endpoint + str(post.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['body'] == data['body']

    
    def test_delete(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.delete(self.endpoint + str(post.public_id) + '/')

        assert response.status_code == status.HTTP_204_NO_CONTENT


    
    def test_list_anonynous(self, client, post):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    

    def test_retrieve_anonymous(self, client, post):
        response = client.get(self.endpoint + str(post.public_id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex

    
    def test_create_anonymous(self, client, post):
        data = {
            'author' : 'test_user',
            'body': 'test post body anonymous'
        }
        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_update_anonymous(self, client, post):
        data = {
            'author' : 'test_user',
            'body': 'test post body anonymous'
        }
        response = client.put(self.endpoint + str(post.public_id) + '/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    
    def test_delete_anonymous(self, client, post):
        response = client.delete(self.endpoint + str(post.public_id) + '/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_like(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(post.public_id) + '/like/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['likes_count'] == 1
        assert response.data['liked'] == True

        response = client.post(self.endpoint + str(post.public_id) + '/remove_like/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['likes_count'] == 0
        assert response.data['liked'] == False
        



