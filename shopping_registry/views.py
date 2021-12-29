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
    # Stores the total purchase price
    total = 0
    # Stores the products
    products = []
    # Stores the quantities, in the same order as to preserve the relationship
    # Considering implementing into a dictionary
    quantities = []
    # Stores the prices
    prices = []
    # Stores individual prices and the price of 100 grams if bulk.
    ind_prices = [] 
    # Stores the name of the product, its individual price and its bulk's boolean
    # value
    dictionary = {}
    # Stores the boolean value to check if it was a bulk product.
    bulk = [] 

    for purchase in purchases:
        # Sums the price to the total
        total += purchase.price
        # Appends the product's name and quantity bough
        products.append(purchase.product)
        quantities.append(purchase.quantity)
        # Verifies bulk value while "purchase" is in memory
        if purchase.bulk == True:
            # Instead of storing price per gram, prices[] stores the price per
            # 100 grams.
            # Consider refactoring
            prices.append((purchase.price / purchase.quantity) * 100)
        else:
            # Stores the price of the product
            prices.append(purchase.price)
        # Stores the bulk value of the product
        bulk.append(purchase.bulk)

    for x in range(0, len(products)):
        # Since bulk was already calculated, check for bulk status and calculate
        # individual price
        if bulk[x] == False:
            ind_prices.append(float((prices[x] / quantities[x])))
        else:
            ind_prices.append(float(prices[x]))
        # Rounds the value to 2 decimal places
        ind_prices[x] = round(ind_prices[x], 2)
        # Generates the dictionary
        dictionary[x] = {'Nombre': products[x], 'Precio': ind_prices[x], 
            'Bulk': bulk[x]}

    context = {'date': date, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary}
    return render(request, 'shopping_registry/date.html', context)