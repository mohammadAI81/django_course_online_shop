from django.urls import path

from .views import payment_process, payment_callback_view

app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='payment-process'),
    path('callback/', payment_callback_view, name='payment-callback')
]

