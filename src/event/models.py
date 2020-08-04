from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    description = models.TextField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.description[:50]
