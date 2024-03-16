from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('comment/<int:pk>/', views.CommentCreteView.as_view(), name='comment-create'),
]
