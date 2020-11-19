from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Feedback(models.Model):
    ua = models.CharField(null=True, blank=True, max_length=256, verbose_name='User agent')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='feedbacks')
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.SET_NULL, related_name='feedbacks')
    location = models.TextField(max_length=256)
    referrer = models.CharField(null=True, blank=True, max_length=128)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{"Anonymous" if not self.user else ""}Feedback from {self.location}'
