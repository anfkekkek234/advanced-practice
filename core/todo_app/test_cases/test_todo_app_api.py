

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def commen_user():
    user = User.objects.create_user(
        email="admin@gmail.com",password="jcjdjr2132@",is_verified= True
    )
    return user



@pytest.mark.django_db
class TestTaskApi:
    
    def test_get_task_response_200_status(self,api_client):
        url = reverse("todo_app:api-v1:task")
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_create_task_response_401_status(self,api_client):
        url = reverse("todo_app:api-v1:task")
        data = {
            "title" : "ali",
            "done" : True,
        }
        response = api_client.task(url,data)
        
    def test_create_task_response_201_status(self,api_client,commen_user):
        url = reverse("todo_app:api-v1:task")
        data = {
            "title" : "ali",
            "done" : True,
        }
        api_client.force_authenticate(user=commen_user)
        response = api_client.task(url,date)
        assert response.status_code == 201
        
    def test_create_task_invalid_data_response_400_status(
        self, api_client, commen_user, 
    ):
        url = reverse("todo_app:api-v1:task")
        data = {
            "title" : "ali",
        }
        api_client.force_authenticate(user=commen_user)
        response = api_client.task(url,data)
        assert response.status_code == 400