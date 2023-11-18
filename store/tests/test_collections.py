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