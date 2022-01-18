from django import forms

from .models import Category, Purchase

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Nombre'}

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity', 'price', 'date_purchase', 'bulk']
        labels = {'product': 'Producto', 'quantity': 'Cantidad', 'price': 'Precio',
            'date_purchase': 'Fecha de compra', 'bulk': 'Granel'}