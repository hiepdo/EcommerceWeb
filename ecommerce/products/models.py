from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Item(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price= models.FloatField(blank= True, null = True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    image = models.ImageField(upload_to='product/',blank= True)
    slug=models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-card", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def total_price(self):
        if self.item.discount_price:
            return self.item.discount_price * self.quantity
        else:
            return self.item.price * self.quantity

    def amount_saved(self):
        return (self.item.price - self.item.discount_price) * self.quantity







class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def final_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price()
        return total


