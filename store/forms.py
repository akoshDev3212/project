from django import forms
from .models import Order

class OrderForm(forms.Form):
    adress = forms.CharField(label='Write your adress',)
    phone = forms.CharField(label='Write your phone number',)

    class Meta:
        model = Order
        fields = ['phone', 'adress']