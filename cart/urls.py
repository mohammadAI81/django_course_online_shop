from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='cart-detail'),
    path('add/<int:product_id>/', views.add_to_cart_view, name='cart-add'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='cart-remove'),
    path('clean/', views.clear_cart, name='cart-clean'),
]

