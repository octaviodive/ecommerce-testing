from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView, View
from .models import Item, OrderItem, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
            messages.error(
                request, ("There was an error, please try again..."))
            return render(request, 'core/login.html', {})
    else:
        return render(request, 'core/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('core:home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after registration
            login(request, user)
            # Redirect to the desired page after registration
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'core/register.html', {'form': form})


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'core/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order_summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:item_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:item_detail", slug=slug)