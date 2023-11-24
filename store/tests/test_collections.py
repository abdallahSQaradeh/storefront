from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db # will ensure the Django database is set up
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # Arange

        # Act
        client = APIClient()
        respnse = client.post('/store/collections/',{'title':'a'})

        # Assert
        assert respnse.status_code  == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        respnse = client.post('/store/collections/',{'title':'a'})

        assert respnse.status_code  == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self):
            client = APIClient()
            client.force_authenticate(user=User(is_staff = True))
            respnse = client.post('/store/collections/',{'title':''})

            # TESTS     should test single thing
            assert respnse.status_code  == status.HTTP_400_BAD_REQUEST
            assert respnse.data['title'] is not None

    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff = True))
        respnse = client.post('/store/collections/',{'title':'a'})

        assert respnse.status_code  == status.HTTP_201_CREATED
        assert respnse.data['id'] > 0