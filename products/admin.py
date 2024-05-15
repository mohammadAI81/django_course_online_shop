from django.contrib import admin

from .models import Product, Comment

from jalali_date.admin import ModelAdminJalaliMixin


class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars']
    extra = 1


@admin.register(Product)
class AdminProduct(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'price', 'active')
    ordering = ('-datetime_created', )
    list_editable = ('active',)
    inlines = [
        CommentInLine,
    ]


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('author', 'product', 'stars', 'active')
    ordering = ('-datetime_created', )
