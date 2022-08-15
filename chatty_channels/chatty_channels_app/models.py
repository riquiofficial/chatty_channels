from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:30]


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    body = models.CharField(max_length=500, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.sender}"
