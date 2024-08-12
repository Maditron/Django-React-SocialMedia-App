import pytest
from core.user.models import User




data_user = {
"username": "test_user",
"email": "test@gmail.com",
"first_name": "Test",
"last_name": "User",
"password": "test_password"
}


data_user2 = {
"username": "test_user2",
"email": "test2@gmail.com",
"first_name": "Test2",
"last_name": "User2",
"password": "test_password2"
}


data_superuser = {
"username": "test_superuser",
"email": "testsuperuser@example.com",
"first_name": "Test",
"last_name": "Superuser",
"password": "test_password"
}


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(**data_superuser)


@pytest.fixture
def user(db):
    return User.objects.create_user(**data_user)


@pytest.fixture
def user2(db):
    return User.objects.create_user(**data_user2)


