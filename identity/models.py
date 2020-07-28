from django.db import models
from django.contrib.auth.models import User
from django.utils.ipv6 import ipaddress
import hashlib

class Shadow(models.Model):
    fingerprint = models.CharField(max_length=2048, unique=True)
    addr = models.GenericIPAddressField(unpack_ipv4=True)
    agent = models.TextField(default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shadow')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'of {self.user.username}'
    
    def save(self, *args, **kwargs):
        self.fingerprint = str(self.calculate_fingerprint(self.addr, self.agent))
        #self.addr = self.addr
        super().save(*args, **kwargs)

    
    @staticmethod
    def calculate_fingerprint(addr, agent, **kwargs):
        raw = f'{addr}@{agent}'
        return hashlib.md5(raw.encode()).hexdigest()
    
    @staticmethod
    def authenticate(request):
        addr = request.META['REMOTE_ADDR']
        agent = request.META['HTTP_USER_AGENT']
        fp = Shadow.calculate_fingerprint(addr, agent)
        qs = Shadow.objects.filter(fingerprint=fp)
        if not qs.exists():
            return None
        else:
            return qs.first()


    @property
    def username(self):
        return self.user.username
    
