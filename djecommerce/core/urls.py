from django.urls import path
from .views import (home,
                    login_user,
                    logout_user,
                    register_user,
                    add_to_cart,
                    remove_from_cart,
                    OrderSummaryView,
                     ItemDetailView) 

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),

]
