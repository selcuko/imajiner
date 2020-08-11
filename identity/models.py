from django.db import models
from django.contrib.auth.models import User
from django.utils.ipv6 import ipaddress
import hashlib
from uuid import uuid4 as uuid
from .methods import remote_addr, fingerprint, user_agent

class Shadow(models.Model):
    fingerprint = models.CharField(max_length=2048, unique=True)
    addr = models.GenericIPAddressField(unpack_ipv4=True)
    agent = models.TextField(default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shadow')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Shadow r/ {self.user.username}'
    
    def save(self, *args, **kwargs):
        self.addr = remote_addr(request)
        self.agent = user_agent(request)
        self.fingerprint = fingerprint(addr=self.addr, agent=self.agent)
        super().save(*args, **kwargs)
    
    @staticmethod
    def create_shadow(request, username=''):
        username = str(username)
        if len(username) < 6: raise Exception('Username too short.')
        shadow = Shadow.objects.create(
            user=User.objects.create(username=username),
            agent=user_agent(request),
            addr=remote_addr(request),
        )
        return shadow
            
    @staticmethod
    def authenticate(request):
        fp = fingerprint(request)
        try:
            return Shadow.objects.get(fingerprint=fp)
        except Shadow.DoesNotExist:
            return None

    
