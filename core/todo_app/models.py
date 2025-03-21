# models.py
from django.db import models

from accounts.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
