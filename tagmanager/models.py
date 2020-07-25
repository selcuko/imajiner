from django.db import models
from django.utils import text
from django.contrib.auth.models import User

class AbstractTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)



class TagManager(models.Model):
    def get(self, slug):
        try:
            return self.tags.get(abstract__slug=slug)
        except ObjectTag.DoesNotExist:
            return None
    def delta(self, slug, diff=1):
        tag = self.get(slug)
        if not tag:
            return False
        tag.delta(diff)
        return True


class ObjectTag(models.Model):
    abstract = models.ForeignKey(AbstractTag, on_delete=models.CASCADE, related_name='objs')
    count = models.IntegerField(default=1)
    manager = models.ForeignKey(TagManager, on_delete=models.CASCADE, related_name='tags')

    def delta(self, diff):
        if not (diff and isinstance(diff, int)):
            return False
        self.count += diff
        self.save()
        return True


class UserTagManager(models.Model):
    issuer = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='tags')

    def delta(self, slug, diff):
        self.individuals.get(objtag__abstract__slug=slug).delta(diff)


class IndividualTag(models.Model):
    count = models.IntegerField(default=1)
    objtag = models.ForeignKey(ObjectTag, on_delete=models.SET_NULL, null=True, related_name='individuals')
    manager = models.ForeignKey(UserTagManager, on_delete=models.SET_NULL, null=True, related_name='individuals')

