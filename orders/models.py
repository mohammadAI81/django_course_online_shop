from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name=_('User'))
    is_paid = models.BooleanField(_('Is paid'), default=False)

    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=15)
    address = models.CharField(_('Address'), max_length=700)

    order_notes = models.CharField(_('Order Notes'), max_length=700, blank=True)

    # Zarin Pal Data
    authority = models.CharField(max_length=255, blank=True)
    ref_id = models.CharField(max_length=150, blank=True)
    zarinpal_data = models.TextField(blank=True)

    datetime_created = models.DateTimeField(verbose_name=_('Datetime Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name=_('Datetime Modified'), auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        result = 0
        for item in self.items.all():
            result += item.quantity * item.price
        return result


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} x {self.quantity} (price:{self.price})'
