from datetime import datetime

from django.test import TestCase

from accounts.models import User , Profile

from ..models import Task

class TestTaskModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email="tests@gmail.com",password="ndasnsdnads@ma2"
        )
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = "aliking",
            last_name = "nsadnas",
            description = "nsdndsn"
        )
        
    def test_create_task_with_valid_data(self):
        task = Task.objects.create(
            user = self.profile,
            title = "hiihkhi",
            done = True
        )
        print(f"Task user type: {type(task.user)}")
        self.assertTrue(Task.objects.filter(pk=task.id).exists())
        self.assertEquals(task.title,"hiihkhi")