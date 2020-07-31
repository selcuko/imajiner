from django.db import models
from django.utils import text
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class AbstractTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name} ({self.slug})'

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)



class TagManager(models.Model):
    def __str__(self):
        return f'of {self.narrative}'

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
    
    def display(self):
        return self.tags.all()[:6]
    
    def has_tags(self):
        return True if self.tags.all().count() > 0 else False


class ObjectTag(models.Model):
    abstract = models.ForeignKey(AbstractTag, on_delete=models.CASCADE, related_name='objs')
    count = models.IntegerField(default=1)
    manager = models.ForeignKey(TagManager, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return f'of {self.manager.narrative} for {self.abstract}'

    def delta(self, diff):
        if not (diff and isinstance(diff, int)):
            return False
        self.count += diff
        self.save()
        return True


class UserTagManager(models.Model):
    issuer = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='tags')

    def __str__(self):
        return f'of {self.issuer}'

    def delta(self, slug, diff, narrative):
        try:
            tag = self.individuals.get(
                objtag__abstract__slug=slug,
                objtag__manager__narrative__slug=narrative,
                )

        except IndividualTag.DoesNotExist:
            if not AbstractTag.objects.filter(slug=slug).exists():
                raise AbstractTag.DoesNotExist('No AbstractTag exists with given slug.')
                        
            objtag = ObjectTag.objects.filter(abstract__slug=slug)
            if not objtag.exists():
                objtag = ObjectTag.objects.create(
                    abstract=AbstractTag.objects.get(slug=slug),
                    manager=TagManager.objects.get(narrative__slug=narrative),
                    count=0,
                )
            else:
                objtag = objtag[0]

            tag = IndividualTag.objects.create(
                objtag=objtag,
                manager=self,
                count=0,
            )
        return tag.delta(diff)

@receiver(post_save, sender=User)
def create_utagman(sender, instance, created, **kwargs):
    """Create UserTagManager for User programmatically."""

    if not created:
        return
    utagman = UserTagManager.objects.create(issuer=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.tags.save()


class IndividualTag(models.Model):
    count = models.IntegerField(default=1)
    objtag = models.ForeignKey(ObjectTag, on_delete=models.SET_NULL, null=True, related_name='individuals')
    manager = models.ForeignKey(UserTagManager, on_delete=models.SET_NULL, null=True, related_name='individuals')

    def __str__(self):
        return f'issued by {self.manager.issuer} for {self.count} times'

    def delta(self, amount):
        self.count += amount
        self.save()
        self.objtag.delta(amount)
        self.objtag.save()
        return True