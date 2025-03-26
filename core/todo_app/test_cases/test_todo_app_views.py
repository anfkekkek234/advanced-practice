
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Profile, User
from todo_app.models import Task


class TestTaskView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="a/mdadmsm"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="ali",
            last_name="nrnfnf",
            description="dnnsdn",
        )
        self.task = Task.objects.create(
            user=self.profile,
            title="hiihkhi",
            done=True
        )

    def test_task_url_successful_response(self):
        url = reverse("todo_app:task_list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "task_list")  # بررسی محتوای صفحه
        self.assertTemplateUsed(response, "todo_app/task_list.html")  # اصلاح شده
