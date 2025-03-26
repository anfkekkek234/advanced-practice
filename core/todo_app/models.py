# models.py
from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Profile

# getting user model project
User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
