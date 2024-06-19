from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

class OrdinaryUser(models.Model):
    STATUS_CHOICES = ((0, "Offline"),
                      (1, "Online"))

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,default=0)
    time = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.username

class Messages(models.Model):

    ord_user = models.ForeignKey(OrdinaryUser, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=1000, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_meta = models.TextField(null=True)
    
    
    def __str__(self):
        return f"{self.ord_user.username}, {self.message}"

    @classmethod
    def get_messages(cls):
        messages = Messages.objects.all().order_by('-timestamp')
        return messages




