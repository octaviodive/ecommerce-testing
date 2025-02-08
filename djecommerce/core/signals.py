from django.db.models.signals import pre_save
from django.utils.text import slugify
from .models import Item

            
def create_slug(instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(create_slug, sender=Item)
