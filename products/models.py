from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = RichTextField(verbose_name=_('Description'))
    short_description = models.TextField(verbose_name=_('Short Description'), blank=True)
    price = models.PositiveIntegerField(verbose_name=_('Price'), default=0)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    image = models.ImageField(verbose_name=_('Product Image'), upload_to='product/product_cover/', blank=True)

    datetime_created = models.DateTimeField(verbose_name=_('Datetime Created'), default=timezone.now)
    datetime_modified = models.DateTimeField(verbose_name=_('Datetime Modified'), auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.pk])


class ActiveCommentsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',
                                verbose_name=_('Comment Product'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments',
                               verbose_name=_('Comment Author'))
    body = models.TextField(verbose_name=_('Comment Text :', ))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is your score ?', ))

    datetime_created = models.DateTimeField(auto_now_add=True, )
    datetime_modified = models.DateTimeField(auto_now=True, )

    active = models.BooleanField(default=True, )
    # Manager
    objects = models.Manager()
    active_comment_manager = ActiveCommentsManager()

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.product.id])

