from django.contrib.auth.models import User
from rest_framework import status
import pytest

@pytest.fixture
def create_collection(api_client):# the parameters here are the fixtures
     
    def do_create_collection(collection):
        return api_client.post("/store/collections/",collection)

    return do_create_collection

@pytest.mark.django_db # will ensure the Django database is set up
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self,create_collection):
        respnse = create_collection({'title':'a'})

        assert respnse.status_code  == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self,authenticate,create_collection):
        authenticate()

        respnse = create_collection({'title':'a'})

        assert respnse.status_code  == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self,authenticate,create_collection):
            authenticate(is_staff=True)

            respnse = create_collection({'title':''})

            # TESTS     should test single thing
            assert respnse.status_code  == status.HTTP_400_BAD_REQUEST
            assert respnse.data['title'] is not None

    def test_if_data_is_valid_returns_201(self,authenticate,create_collection):
        authenticate(is_staff=True)
        respnse = create_collection({'title':'a'})

        assert respnse.status_code  == status.HTTP_201_CREATED
        assert respnse.data['id'] > 0