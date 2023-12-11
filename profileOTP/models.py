from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='photos/qrcode/', null=True)
    is_qr_code_scanned = models.BooleanField(default=False)