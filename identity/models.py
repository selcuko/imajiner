from django.db import models
from django.contrib.auth.models import User
from django.utils.ipv6 import ipaddress
import hashlib
from uuid import uuid4 as uuid

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
    
    def create_shadow(request, username=None):
        if not isinstance(username, str):
            username = str(uuid())
        addr = Shadow.get_ip(request)
        shadow = Shadow.objects.create(
            user=User.objects.create(username=username),
            agent=request.META.get('HTTP_USER_AGENT', ''),
            addr=addr,
        )
        return shadow
            

    @staticmethod
    def get_ip(request):
#        print('META', request.META)
        addr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if addr: return addr
        addr = request.META.get('REMOTE_ADDR', None)
        if addr: return addr
        raise Exception('Could not acquire remote address from request.')
    @staticmethod
    def calculate_fingerprint(addr, agent, **kwargs):
        raw = f'{addr}@{agent}'
        return hashlib.md5(raw.encode()).hexdigest()
    
    @staticmethod
    def authenticate(request):
        addr = Shadow.get_ip(request)
        agent = request.META.get('HTTP_USER_AGENT', '')
        fp = Shadow.calculate_fingerprint(addr, agent)
        qs = Shadow.objects.filter(fingerprint=fp)
        if not qs.exists():
            return None
        else:
            return qs.first()


    @property
    def username(self):
        return self.user.username
    
