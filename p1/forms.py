from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    pickup_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Order
        fields = ['pickup_time', 'name', 'phone']