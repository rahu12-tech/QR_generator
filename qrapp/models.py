from django.db import models
from django.contrib.auth.models import User
import uuid

class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    qr_image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20, default='black')
    background_color = models.CharField(max_length=20, default='white')
    is_active = models.BooleanField(default=True)
    scans = models.IntegerField(default=0)
    short_code = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = uuid.uuid4().hex[:6]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s QR Code for {self.url}"
