from django.forms import ModelForm, Textarea, NumberInput

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'order_notes']

        widgets = {
            'address': Textarea(attrs={'rows': 5}),
            'order_notes': Textarea(attrs={'rows': 3}),
            'phone_number': NumberInput(),
        }
