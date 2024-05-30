from django.db import models
from .user import MyUser

class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
