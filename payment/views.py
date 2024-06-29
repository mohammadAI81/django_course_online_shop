from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponseBadRequest

import requests
import json

from orders.models import Order


def payment_process(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    request_header = {
        'accept': 'applications/json',
        'content-type': 'application/json',
    }

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payman/request.json'
    request_data = {
        'merchant_id': settings.ZARINPAL_URL,
        'amount': rial_total_price,
        'description': f'# {order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': '127.0.0.1:8000'
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = res.json()['data']
    authority = data['authority']
    order.authority = authority
    order.save()

    if len(res.json()['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponseBadRequest('errors from zarinpal')
