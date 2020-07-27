from django.db import models
from django.contrib.auth.models import User

class Shadow(models.Model):
    fingerprint = models.CharField(max_length=2048)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shadow')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'of {self.user.username}'
    
    @property
    def username(self):
        return self.user.username
    
