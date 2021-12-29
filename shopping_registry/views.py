from django.shortcuts import render

from .models import Date

def index(request):
    """The home page for Grocery Registry."""
    return render(request, 'shopping_registry/index.html')

def dates(request):
    """Shows all dates."""
    dates = Date.objects.order_by('date_trip')
    context = {'dates': dates}
    return render(request, 'shopping_registry/dates.html', context)

def date(request, date_id):
    """Show a single date and its details."""
    date = Date.objects.get(id=date_id)
    purchases = date.purchase_set.order_by('product')
    total = 0
    products = []
    quantities = []
    prices = []
    ind_prices = [] # Stores individual prices and the price of 100 grams if bulk.
    dictionary = {}
    bulk = [] # Stores the boolean value to check if it was a bulk product.

    for purchase in purchases:
        total += purchase.price
        if purchase.product not in products:
            products.append(purchase.product)
        quantities.append(purchase.quantity)
        if purchase.bulk == True:
            prices.append((purchase.price / purchase.quantity) * 100)
        else:
            prices.append(purchase.price)
        bulk.append(purchase.bulk)

    for x in range(0, len(products)):
        ind_prices.append(float((prices[x] / quantities[x])))
        dictionary[x] = {'Nombre': products[x], 'Precio': ind_prices[x], 
            'Bulk': bulk[x]}

    context = {'date': date, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary}
    return render(request, 'shopping_registry/date.html', context)