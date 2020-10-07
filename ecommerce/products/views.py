from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
from requests import request

from .models import Item,Order,OrderItem
from django.views.generic import ListView,DetailView,View
# Create your views here.


class HomeView(ListView):
    model= Item
    paginate_by = 5
    template_name = "products/home-page.html"

class OrderSummary(LoginRequiredMixin,View):
    def get(self,request):
        try:
            order = Order.objects.get(user = request.user , ordered = False)
            return render(request, "products/order-summary.html", {"order": order})
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order.")
            return redirect("/")




class ItemDetailView(DetailView):
    model= Item
    template_name = "products/product-page.html"

class CheckOutView(View):
    def get(self, *args,**kwargs):
        form = CheckoutForm()
        context = {
            'form' : form
        }
        return render(self.request,"products/checkout-page.html",context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print("The form is valid")
            return redirect('check-out')
        return redirect('check-out')


@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)
    order_item,create = OrderItem.objects.get_or_create(
        user = request.user,
        item = item,
        ordered = False
    )
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was updated quantity in your cart.")
            return redirect("product",slug = slug)
        else:
            order.items.add(order_item)
            messages.info(request,"This item was added in your cart.")
            return redirect("product", slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user = request.user,
            ordered_date = ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "This item was added in your cart.")
        return redirect("product",slug = slug)

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                user = request.user,
                item = item,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your card.")
        else:
            messages.info(request, "This item was not in your card.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)
    return redirect("product", slug=slug)
