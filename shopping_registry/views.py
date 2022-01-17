from django.shortcuts import render
from django.core import serializers
from django.db.models import Sum

from .models import Date, Product, Category, Purchase

import plotly.graph_objects as go

import json
import datetime

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
    # Stores the categories of all the products bought in the trip.
    # The function of this list is to pass it to the Django template, and there,
    # uses this list to verify that a key/value pair relates to the product's
    # category. It's also responsible for the Category/TotalCost visualization
    categories = []
    # Dictionary to store the category of the product coupled with the total
    # spent on that category
    category_spent = {}
    # Stores the boolean value to check if it was a bulk product.
    bulk = [] 

    for purchase in purchases:
        # Sums purchase's price to the total.
        total += purchase.price
        # Stores the product's name, quantity, price and if it's either bought in
        # bulk or not.
        # Stores the product model, it only contains the name and the category
        products.append(purchase.product)
        quantities.append(purchase.quantity)
        prices.append(purchase.price)
        bulk.append(purchase.bulk)

    for x in range(0, len(products)):
        # Stores the categories of the products, checks if the category has been
        # previously added, omits it if it has.
        if products[x].category not in categories:
            categories.append(products[x].category)
        # Creating dictionary to store the total spent per category
        category_spent[products[x].category] = 0
        # Check for bulk status and calculate pricer per unit.
        if bulk[x] == True:
            # If it was a bulk purchase, multiply by 100 to display the price per
            # 100 grams.
            ind_prices.append(float((prices[x] / quantities[x]) * 100))
        else:
            ind_prices.append(float((prices[x] / quantities[x])))
        # Rounds the value to 2 decimal places.
        ind_prices[x] = round(ind_prices[x], 2)
        # Generates a dictionary to store a product's details.
        dictionary[x] = {'Nombre': products[x], 'Categoria': products[x].category,
            'Bulk': bulk[x], 'Precio': ind_prices[x]}

    # Calculating total spent per category
    for purchase in purchases:
        category_spent[purchase.product.category] += purchase.price

    # Product and Price visualization
    # Serialize into JSON the product list QuerySet.
    product_json = serializers.serialize("json", products)
    # Converts JSON into a dict.
    product_dict = json.loads(product_json)
    # List to store the products name to use as tags for the graph.
    product_names = [product['fields']['name'] for product in product_dict]
    # Convert the prices list QuerySet to a list of floats.
    prices_float = [float(price) for price in prices]

    # Generate the Bar chart.
    Bar = go.Bar(x=product_names, y=prices_float)
    layout = go.Layout(title="Productos y costo", xaxis={'title':'Productos'}, 
        yaxis={'title':'Costo'})
    figure = go.Figure(data=[Bar],layout=layout)
    bar_graph = figure.to_html()

    # Total spent per category visualization
    # Serialize into JSON the category list QuerySet.
    category_json = serializers.serialize("json", categories)
    # Converts JSON into a dict.
    category_dict = json.loads(category_json)
    # List to store the categories name.
    category_names = [category['fields']['name'] for category in category_dict]
    # Obtains the values from the category_spent dict and stores them.
    category_values = category_spent.values()
    # List to read and store the values per category and convert them to float.
    total_cat_spent = [value for value in category_values]

    # Generate the Pie chart.
    Pie = go.Pie(labels=category_names, values=total_cat_spent, hole=.3, 
        title_text="Categorias")
    pie_chart = go.Figure(data=Pie)
    pie_graph = pie_chart.to_html()

    context = {'date': date, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary,
        'categories': categories, 'category_spent': category_spent, 
        'bar_graph': bar_graph, 'pie_graph': pie_graph}
    return render(request, 'shopping_registry/date.html', context)

def MonthView(request, year, month):
    """Displays all shopping trips in a month."""
    # QuerySet to store the filtered Dates.
    dates = Date.objects.filter(date_trip__year=year,
        date_trip__month=month)
    # Stores the total spent in the given month.
    total = 0
    # Stores the products bought and the total spent on them.
    products_total = {}
    # Stores the categories of the bought products and the total spent.
    categories_total = {}
    # Initializes the 'purchases' variable and stores an empty QuerySet.
    purchases = Date.objects.none()

    for date in dates:
        # Calculates total spent in the given month.
        total_price = date.purchase_set.order_by('product').aggregate(Sum('price'))
        if total_price['price__sum'] is None:
            pass
        else:
            total += total_price['price__sum']
        # Stores all purchases in the purchases variable as a QuerySet.
        purchases = purchases | date.purchase_set.order_by('product')

    # Rounds the total to 2 decimal places.
    total = round(total, 2)

    for purchase in purchases:
            # Initializes dictionaries.
            products_total[purchase.product.name] = 0
            categories_total[purchase.product.category.name] = 0
    
    for purchase in purchases:
            # Calculates total per product.
            products_total[purchase.product.name] += purchase.price
            # Calculates total per category.
            categories_total[purchase.product.category.name] += purchase.price

    # Stores the datetime value to export to the template.
    date = datetime.datetime(year, month, 1)

    # Stores keys and values from dict to use as labels and values in the charts.
    # Bar chart.
    bar_labels = products_total.keys()
    bar_values = products_total.values()
    # Pie chart.
    pie_labels = categories_total.keys()
    pie_values = categories_total.values()

    # Casts into list for chart compatibility.
    # Bar chart.
    bar_labels = list(bar_labels)
    bar_values = list(bar_values)
    # Pie chart.
    pie_labels = list(pie_labels)
    pie_values = list(pie_values)

    # Generating the charts.
    # Bar chart.
    Bar = go.Bar(x=bar_labels, y=bar_values)
    layout = go.Layout(title="Productos y costo", xaxis={'title':'Productos'}, 
        yaxis={'title':'Costo'})
    figure = go.Figure(data=[Bar],layout=layout)
    bar_graph = figure.to_html()

    # Pie chart.
    Pie = go.Pie(labels=pie_labels, values=pie_values, hole=.3, 
        title_text="Categorias")
    pie_chart = go.Figure(data=Pie)
    pie_graph = pie_chart.to_html()

    context = {'date': date, 'dates': dates, 'total':total, 
        'products_total': products_total, 'bar_graph': bar_graph, 
        'pie_graph':pie_graph}
    return render(request, 'shopping_registry/month_view.html', context)

def Years(request):
    """Shows all years with registered purchases."""
    dates = Date.objects.order_by('date_trip')
    years = []
    for date in dates:
        if date.date_trip.year not in years:
            years.append(date.date_trip.year)
    context = {'years': years}
    return render(request, 'shopping_registry/years.html', context)

def Months(request, year):
    """Shows all the months with registered purchases in the selected month."""
    dates = Date.objects.order_by('date_trip')
    months = []
    for date in dates:
        if date.date_trip.month not in months:
            if date.date_trip.year == year:
                months.append(date.date_trip.month)
    # Find a way to turn the int value to a month datetime.
    context = {'months': months}
    return render(request, 'shopping_registry/months.html', context)