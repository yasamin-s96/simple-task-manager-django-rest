from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest
from model_bakery import baker


User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def other_user():
    return baker.make(User)


@pytest.fixture
def auth_user():
    return baker.make(
        User, username="test", email="test@test.com", password="kjhfkf454@"
    )


@pytest.fixture
def authenticate(client, auth_user):
    client.force_authenticate(user=auth_user)
