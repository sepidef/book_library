from django.db import models
from users.models import CustomUser


class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} by {self.author}"
