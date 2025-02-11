from django.core.cache import cache  # Import the cache module
from django.shortcuts import render, redirect  # Import the render function
from django.views.generic.detail import DetailView
from . models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    items = Item.objects.all()
    return render(request, 'core/home.html', {'items': items})

# class OrderSummaryView(LoginRequiredMixin, View):


class ItemDetailView(DetailView):
    model = Item
    template_name = "core/product.html"
    context_object_name = 'item'


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('core:home')
        else:
            messages.error(request, ("There was an error, please try again..."))
            return render(request, 'core/login.html', {})
    else:
        return render(request, 'core/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('core:home')

     
