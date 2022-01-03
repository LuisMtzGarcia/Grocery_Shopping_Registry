from django.shortcuts import render

from .models import Date, Product, Category

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
    all_products = Product.objects.all()
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
    # Stores the categories of all the products bought in the trip
    categories = []
    # Dictionary to store the category of the product coupled with the total
    # spent on that category
    category_spent = {}
    # Stores the boolean value to check if it was a bulk product.
    bulk = [] 

    for purchase in purchases:
        # Sums the price to the total
        total += purchase.price
        # Appends the product's name and quantity bought
        # Stores the product model, it only contains the name and the category
        products.append(purchase.product)
        quantities.append(purchase.quantity)
        # Stores the price of the product
        prices.append(purchase.price)
        # Stores the bulk value of the product
        bulk.append(purchase.bulk)

    for x in range(0, len(products)):
        # Stores the categories of the products, checks if the category has been
        # previously added, omits it if it has.
        if products[x].category not in categories:
            categories.append(products[x].category)
        # Since bulk was already calculated, check for bulk status and calculate
        # individual price
        if bulk[x] == True:
            ind_prices.append(float((prices[x] / quantities[x]) * 100))
        else:
            ind_prices.append(float((prices[x] / quantities[x])))
        # Rounds the value to 2 decimal places
        ind_prices[x] = round(ind_prices[x], 2)
        # Generates the dictionary
        dictionary[x] = {'Nombre': products[x], 'Categoria': products[x].category,
            'Bulk': bulk[x], 'Precio': ind_prices[x]}

    # Obtaining total spent per category
    # Creating the dictionary
    for category in categories:
        category_spent[category] = 0
    # Obtaining the total per category
    for purchase in purchases:
        category_spent[purchase.product.category] += purchase.price


    context = {'date': date, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary,
        'categories': categories, 'category_spent': category_spent}
    return render(request, 'shopping_registry/date.html', context)