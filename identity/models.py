from django.db import models
from django.contrib.auth.models import User
from django.utils.ipv6 import ipaddress
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
from uuid import uuid1
from .methods import remote_addr, fingerprint, user_agent

class Shadow(models.Model):
    fingerprint = models.CharField(max_length=2048, unique=True)
    addr = models.GenericIPAddressField(unpack_ipv4=True)
    agent = models.TextField(default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shadow')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Shadow u/{self.user.username}'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def become_author(self, password):
        self.user.set_password(password)
        self.user.save()
        self.active = False
        self.save()
        return self.user
    
    @staticmethod
    def create_shadow(request, fingerprint, username=''):
        if username:
            username = str(username)
        else:
            username = str(uuid1())
        if len(username) < 6: raise Exception('Username too short.')
        shadow = Shadow.objects.create(
            user=User.objects.create(username=username),
            agent=user_agent(request),
            addr=remote_addr(request),
            fingerprint=fingerprint,
        )
        return shadow
            
    @staticmethod
    def authenticate(fingerprint):
        try:
            return Shadow.objects.get(fingerprint=fingerprint)
        except Shadow.DoesNotExist:
            return None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    
