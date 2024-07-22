from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from .form import OrderForm
from .models import OrderItem

from cart.cart import Cart


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _("You can't go because your cart empty"))
        return redirect('product-list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST, )
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            messages.success(request, _('your Order Submit Successfully'))

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
            cart.clean()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payment:payment-process')

    context = {
        'form': order_form
    }

    return render(request, 'orders/orders_create.html', context)
