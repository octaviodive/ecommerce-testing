from django.contrib import admin
from . models import UserProfile, Item, OrderItem, Address, Payment, Coupon, Order, Refund
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(Refund)