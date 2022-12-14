from django.utils.text import slugify
import random

def slugify_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.Title)
    klass = instance.__class__
    qs = klass.objects.filter(Slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(100000, 900000)
        slug = f"{slug}-{rand_int}"
   