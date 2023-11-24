from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

# we add here just the fixtures that is going to be used accross all tests modules

# this function will be passed as a parmeter to the tests (As its value executed)
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):

    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff = is_staff))
    
    return do_authenticate