from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerCmd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command_text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_command = models.ForeignKey(CustomerCmd, on_delete=models.CASCADE)
    reply_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)