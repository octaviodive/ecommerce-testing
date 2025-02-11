from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Item, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


            
def create_slug(instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(create_slug, sender=Item)
