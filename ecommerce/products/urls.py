from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    CheckOutView,
    add_to_cart,
    remove_from_cart,
    OrderSummary
)


urlpatterns = [
    path('',HomeView.as_view(),name="item-list"),
    path('product/<slug>/',ItemDetailView.as_view(),name='product'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name= 'remove-from-cart'),
    path('order-summary/',OrderSummary.as_view(),name = 'order-summary'),
    #path('checkout/',CheckOutView.as_view(),name='check-out')
    path('check-out/',CheckOutView.as_view(),name='check-out')
]