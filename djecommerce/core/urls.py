from django.urls import path
from .views import (home,
                    login_user,
                    logout_user,
                     ItemDetailView) 

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
