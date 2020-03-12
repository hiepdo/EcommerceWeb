from django.urls import path
from .views import HomeView,ItemDetailView,CheckOut


urlpatterns = [
    path('',HomeView.as_view(),name="item-list"),
    path('product/<slug>/',ItemDetailView.as_view(),name='product'),
    path('checkout/',CheckOut.as_view(),name='check-out')
]