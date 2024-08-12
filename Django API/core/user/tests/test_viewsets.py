import pytest
from core.fixtures.user import user, user2, superuser
from rest_framework import status
from conftest import client

class TestUserViewset:

    endpoint = '/api/v1/user/'


    def test_list(self, client, user, user2, superuser):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2



    def test_list_superuser(self, client, user, user2, superuser):
        client.force_authenticate(user=superuser)

        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3
    

    def test_retrieve(self, client, user, user2):
        client.force_authenticate(user=user)

        response = client.get(self.endpoint + str(user2.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user2.public_id.hex
        assert response.data['username'] == user2.username
        assert response.data['email'] == user2.email

    
    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            'username': "user3",
            "email": "user3@example.com",
            "password": "User1234"
        }
        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    
    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            'username': "user3",
            "email": "user3@example.com",
            "password": "User1234"
        }
        response = client.put(self.endpoint + str(user.public_id) + '/', data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        data = {
            'username': "new username"
        }
        
        response = client.patch(self.endpoint + str(user.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
    

    def test_bah(self, client, user, user2):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + '?username=test_user') 
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['username'] == 'test_user'
         

