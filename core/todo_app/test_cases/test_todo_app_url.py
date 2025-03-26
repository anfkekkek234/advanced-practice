from django.test import SimpleTestCase
from django.urls import resolve , reverse

from ..views import TaskListView

#  Create your tests here.

class TestUrl(SimpleTestCase):
    def test_list_task_todoapp_url_resolve(self):
        url = reverse("todo_app:task_list")
        self.assertEquals(resolve(url).func.view_class,TaskListView)