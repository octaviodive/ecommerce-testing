from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from .choices import AddressChoices, CategoryChoices, LabelChoices, enum_to_choices

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    discount_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    category = models.CharField(choices=enum_to_choices(CategoryChoices), max_length=2)
    label = models.CharField(choices=enum_to_choices(LabelChoices), max_length=1)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        if self.item.discount_price is None:
            return 0.0
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name='quantity_gte_1')
        ]


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    street_address = models.CharField(max_length=100, verbose_name="Street Address")
    apartment_address = models.CharField(max_length=100, verbose_name="Apartment Address")
    country = CountryField(multiple=False, verbose_name="Country")
    zip = models.CharField(max_length=20, verbose_name="ZIP Code")
    address_type = models.CharField(max_length=1, choices=enum_to_choices(AddressChoices), verbose_name="Address Type")
    default = models.BooleanField(default=False, verbose_name="Default")

    def __str__(self):
        return f"{self.user.username} - {self.get_address_type_display()}"

    class Meta:
        verbose_name_plural =  'Addresses'


class Payment(models.Model):
    payment_charge_id = models.CharField(max_length=50, verbose_name="Payment Charge ID")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="User")
    amount = models.FloatField(verbose_name="Amount")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    


    
                       
