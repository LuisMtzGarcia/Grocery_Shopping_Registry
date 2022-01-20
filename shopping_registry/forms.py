from django import forms

from .models import Category, Purchase, Product, Date

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name']
        labels = {'category': 'Categoria', 'name': 'Nombre'}

class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['date_trip']
        labels = {'date_trip': 'Fecha de la compra'}