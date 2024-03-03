from django.contrib import admin

from .models import Product, Comment


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'active')
    ordering = ('-datetime_created', )
    list_editable = ('active',)


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('author', 'product', 'stars', 'active')
    ordering = ('-datetime_created', )
