from django import forms

from .models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'category', 'quantity', 'price', 'date_purchase', 'bulk']
        labels = {'product': 'Producto','category': 'Categoria', 'quantity': 'Cantidad', 'price': 'Precio',
            'date_purchase': 'Fecha de compra', 'bulk': 'Granel'}
