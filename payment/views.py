from django.shortcuts import get_object_or_404, redirect, reverse
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse

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

    request_data = {
        'MerchantID': 'aaancdksaaancdksaaancdksaaancdksmoc4',
        'Amount': rial_total_price,
        'Description': f'# {order.id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': 'http://127.0.0.1:8000' + reverse('payment:payment-callback')
    }
    
    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    
    print(res)
    data = res.json()
    print(data)
    
    authority = data['Authority']
    order.authority = authority
    order.save()

    if 'errors' not in res.json():
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponseBadRequest('errors from zarinpal')


def payment_callback_view(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'applications/json',
            'content-type': 'application/json',
        }

        request_data = {
            'MerchantID': 'aaancdksaaancdksaaancdksaaancdksmoc4',
            'Amount': rial_total_price,
            'Authority': payment_authority
        }
        zarinpal_verify_request = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'

        req = requests.post(url=zarinpal_verify_request, data=json.dumps(request_data), headers=request_header)
        print(req.json())

        if 'errors' not in req.json(): # No Sandbox  "and data in req.json()"
            data = req.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد')
            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد. البته این تراکنش قبلا انجام شده.')
            else:
                # error_code = req.json()['errors']['code']
                # error_message = req.json()['errors']['message']
                return HttpResponse(f' تراکنش ناموفق بود')
    else:
        # error_code = req.json()['errors']['code']
        # error_message = req.json()['errors']['message']
        return HttpResponse(f' تراکنش ناموفق بود')





