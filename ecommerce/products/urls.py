from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    CheckOut,
    add_to_cart,
    remove_from_cart
)


urlpatterns = [
    path('',HomeView.as_view(),name="item-list"),
    path('product/<slug>/',ItemDetailView.as_view(),name='product'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name= 'remove-from-cart'),
    path('checkout/',CheckOut.as_view(),name='check-out')
]