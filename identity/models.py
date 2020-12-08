from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.ipv6 import ipaddress
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres import fields
import hashlib
from uuid import uuid1
from .methods import remote_addr, fingerprint, user_agent
from django.contrib.auth import user_logged_in, user_logged_out

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
    languages = fields.ArrayField(models.CharField(max_length=5), null=True, blank=True)
    preferences = models.JSONField(default=dict)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class LoggedInUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_in')
    user_agent = models.TextField(null=True, blank=True)
    session_key = models.CharField(max_length=32)

    def __str__(self): return f'{self.user.username}-{self.session_key}'


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    if not request.session.session_key:
        request.session.save()
    
    LoggedInUser.objects.get_or_create(
        user=kwargs.get('user'), 
        session_key=request.session.session_key,
        user_agent=user_agent(request),
    ) 

    
