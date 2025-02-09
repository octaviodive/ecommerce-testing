from django.core.cache import cache  # Import the cache module
from django.shortcuts import render  # Import the render function
from . models import Item


def home(request):
    items = Item.objects.all()
    return render(request, 'core/home.html', {'items': items})
