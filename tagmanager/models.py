from django.db import models
from django.utils import text
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class AbstractTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f'Abstract Tag: {self.name} ({self.slug})'

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name, allow_unicode=False)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tag:detail', kwargs={'slug':self.slug})



class TagManager(models.Model):
    def __str__(self):
        return f'Tag Manager: {self.narrative.slug}'
     
    def for_user(self, user, count=6):
        """customized tags for user"""
        # if user.is_anonymous:
        return self.tags.filter(count__gt=0)[:count]
    
    def all(self):
        return self.tags.all()
    
    def has_tags(self):
        return self.all().exists()
    
    def add(self, abstract):
        if isinstance(abstract, str): abstract = AbstractTag.objects.get(slug=abstract)
        return ObjectTag.objects.create(
            abstract=abstract,
            count=0,
            manager=self,
        )
    
    def get(self, abstract):
        try:
            return self.tags.filter(abstract__slug=abstract) 
        except ObjectTag.DoesNotExist:
            return None




class ObjectTag(models.Model):
    abstract = models.ForeignKey(AbstractTag, on_delete=models.CASCADE, related_name='individuals')
    count = models.IntegerField(default=1)
    manager = models.ForeignKey(TagManager, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return f'Object Tag: {self.manager.narrative.slug}'

class UserTagManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='tags')

    def __str__(self):
        return f'User Tag Manager: {self.user.username}'

    def for_narrative(self, slug):
        return self.individuals.filter(object__manager__narrative__slug=slug)
    
    def delta_for(self, abstract, narrative, delta=0):
        try:
            if isinstance(abstract, str): abstract = AbstractTag.objects.get(slug=abstract)
            if isinstance(narrative, str): narrative = Narrative.objects.get(slug=narrative)

            individual = self.individuals.get(
            object__abstract=abstract,
            object__manager__narrative=narrative
        )
        except IndividualTag.DoesNotExist:
            individual = IndividualTag.objects.create(
                manager=self,
                count=0,
                object=ObjectTag.objects.get(manager__narrative=narrative, abstract=abstract),
            )
        individual.count += delta
        individual.save()
        individual.object.count += delta
        individual.object.save()
        return individual.count
    
    def is_interacted_with(self, abstract, slug=''):
        qs = self.individuals.filter(object__abstract__slug=abstract)
        if slug: qs = qs.filter(object__manager__narrative__slug=slug)
        return qs.exists()


@receiver(post_save, sender=User)
def create_utagman(sender, instance, created, **kwargs):
    if not created:
        return
    manager = UserTagManager.objects.create(user=instance)


class IndividualTag(models.Model):
    count = models.IntegerField(default=1)
    object = models.ForeignKey(ObjectTag, on_delete=models.SET_NULL, null=True, related_name='individuals')
    manager = models.ForeignKey(UserTagManager, on_delete=models.SET_NULL, null=True, related_name='individuals')
    
    def __str__(self):
        return f'Individual Tag: [{self.object.abstract.slug}] {self.manager.user.username}@{self.object.manager.narrative.slug}'

    @property
    def effective(self):
        return self.count > 0