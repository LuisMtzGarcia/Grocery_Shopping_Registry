from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core import serializers
from django.db.models import Sum

from .models import Product, Category, Purchase
from .forms import CategoryForm, PurchaseForm, ProductForm

import plotly.graph_objects as go

import json
import datetime

def test_account(username):
    """Checks if the user is using the test account."""
    if username == 'supercuenta':
        raise Http404

def index(request):
    """The home page for Grocery Registry."""
    return render(request, 'shopping_registry/index.html')

@login_required
def dates(request):
    """Shows all dates."""
    # Initializes the list to store the dates with registered purchases.
    dates = []
    # Stores the purchases of the user to extract the dates.
    purchases = Purchase.objects.filter(owner=request.user).order_by('-date_purchase')
    # Extracts the dates of the purchases.
    for purchase in purchases:
        if purchase.date_purchase not in dates:
            dates.append(purchase.date_purchase)

    context = {'dates': dates}
    return render(request, 'shopping_registry/dates.html', context)

@login_required
def date(request, date):
    """Shows all the information for a day's purchases."""
    # Checks if the date parameter is a datetime value to initialize variables.
    if isinstance(date, datetime.date):
        # Stores the date as a string.
        date_string = datetime.datetime.strftime(date, '%Y-%m-%d')
    else:
        # Stores the date as a string.
        date_string = date
        # If the date is string, converts it into datetime value.
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    # Gets all the purchases made on the selected date.
    purchases = Purchase.objects.filter(date_purchase=date, owner=request.user)
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
        if products[x] in dictionary:
            dictionary[x]
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

    context = {'date': date, 'date_string': date_string, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary,
        'categories': categories, 'category_spent': category_spent, 
        'bar_graph': bar_graph, 'pie_graph': pie_graph}
    return render(request, 'shopping_registry/date.html', context)

@login_required
def edit_purchase(request, purchase_id):
    """Edit an existing purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)   

    # Make sure the purchase belongs to the current user.
    if purchase.owner != request.user:
        raise Http404

    date = purchase.date_purchase

    if request.method != 'POST':
        # Initial request; pre-fill form with the current purchase.
        form = PurchaseForm(instance=purchase)
    else:
        # POST data submitted; process data.
        form = PurchaseForm(instance=purchase, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_registry:date', date=date)

    context = {'purchase': purchase, 'form': form}
    return render(request, 'shopping_registry/edit_purchase.html', context)

@login_required
def edit_category(request, category_name):
    """Edit an existing category."""
    category = get_object_or_404(Category, name=category_name)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Make sure the category belongs to the current user.
    if category.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current category.
        form = CategoryForm(instance=category)
    else:
        # POST data submitted; process data.
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_registry:dates')

    context = {'category': category, 'form': form}
    return render(request, 'shopping_registry/edit_category.html', context)

@login_required
def edit_product(request, product_id):
    """Edit an existing product."""
    product = get_object_or_404(Product, id=product_id)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Make sure the product belongs to the current user.
    if product.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current product.
        form = ProductForm(instance=product)
    else:
        # POST data submitted; process data.
        form = ProductForm(instance=product, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_registry:dates')

    context = {'product': product, 'form': form}
    return render(request, 'shopping_registry/edit_product.html', context)

@login_required
def erase_date_confirmation(request, date_string):
    """Confirm the deletion of the purchases done on the selected date."""
    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Gets all the purchases done on the selected date.
    purchases = Purchase.objects.filter(date_purchase=date_string, owner=request.user)

    # Date is stored in string 'YYYY-MM-DD', converted to datetime value.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    context = {'date': date, 'purchases': purchases, 'date_string': date_string}
    return render(request, 'shopping_registry/erase_date_confirmation.html', context)

@login_required
def erase_date(request, date_string):
    """Delete all the purchases done on the selected date."""
    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Date_string is stored in string format 'YYYY-MM-DD', converted to datetime value.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    # Gets all the purchases done on the selected date.
    purchases = Purchase.objects.filter(date_purchase=date_string, owner=request.user)

    # Erases all the queryied purchases.
    purchases_erase = purchases.delete()

    context = {'date': date, 'purchase': purchases}
    return render(request, 'shopping_registry/erase_date.html', context)

@login_required
def delete_purchase_confirmation(request, purchase_id):
    """Confirms the deletion of a purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Make sure the purchase belongs to the current user.
    if purchase.owner != request.user:
        raise Http404

    context = {'purchase': purchase}
    return render(request, 'shopping_registry/delete_purchase_confirmation.html', 
        context)    

@login_required
def delete_purchase(request, purchase_id):
    """Deletes a single purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Make sure the purchase belongs to the current user.
    if purchase.owner != request.user:
        raise Http404

    # Deletes the queryied purchase.
    purchase_erase = purchase.delete()

    context = {'purchase': purchase}
    return render(request, 'shopping_registry/delete_purchase.html', context)

@login_required
def delete_product_confirmation(request, product_id):
    """Confirms the deletion of a product."""
    product = get_object_or_404(Product, id=product_id)

    # Make sure the  user isn't using the test account.
    test_account(request.user.username)

    # Make sure the product belongs to the current user.
    if product.owner != request.user:
        raise Http404

    context = {'product': product}
    return render(request, 'shopping_registry/delete_product_confirmation.html', context)

@login_required
def delete_product(request, product_id):
    """Deletes a single product."""
    product = get_object_or_404(Product, id=product_id)

    # Make sure the product belongs to the current user.
    if product.owner != request.user:
        raise Http404
    
    # Deletes the queryied product.
    product_erase = product.delete()

    context = {'product': product}
    return render(request, 'shopping_registry/delete_product.html', context)

@login_required
def delete_category_confirmation(request, category_id):
    """Confirms the deletion of a category."""
    category = get_object_or_404(Category, id=category_id)

    # Make sure the category belongs to the current user.
    if category.owner != request.user:
        raise Http404

    # Queryies the products related to the category.
    products = category.product_set.all()

    context = {'category': category, 'products': products}
    return render(request, 'shopping_registry/delete_category_confirmation.html', context)

@login_required
def delete_category(request, category_id):
    """Deletes a single category."""
    category = get_object_or_404(Category, id=category_id)

    # Make sure the category belongs to the current user.
    if category.owner != request.user:
        raise Http404

    # Queryies the products related to the category.
    products = category.product_set.all()

    # Deletes the category.
    category_erase = category.delete()

    context = {'category': category, 'products': products}
    return render(request, 'shopping_registry/delete_category.html', context)    

@login_required
def MonthView(request, year, month):
    """Displays all shopping trips in a month."""
    # QuerySet to store the filtered purchases.
    purchases = Purchase.objects.filter(date_purchase__year=year, 
        date_purchase__month=month, owner=request.user)
    # Stores the total spent in the given month.
    total = 0
    # Stores the dates with registered purchases.
    dates = []
    # Stores the products bought and the total spent on them.
    products_total = {}
    # Stores the categories of the bought products and the total spent.
    categories_total = {}

    for purchase in purchases:
        # Calculates the total spent in the month.
        total += purchase.price
        # Initializes dictionaries.
        products_total[purchase.product.name] = 0
        categories_total[purchase.product.category.name] = 0
        # Stores the dates.
        if purchase.date_purchase not in dates:
            dates.append(purchase.date_purchase)
        # Code to cleanup
        """
        # Converts the dates into strings and stores it.
        if purchase.date_purchase.strftime('%Y-%m-%d') not in dates:
            dates.append(purchase.date_purchase.strftime('%Y-%m-%d'))
        """

    # Rounds the total to 2 decimal places.
    total = round(total, 2)

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
        'products_total': products_total, 'categories_total': categories_total,
        'bar_graph': bar_graph, 'pie_graph':pie_graph}
    return render(request, 'shopping_registry/month_view.html', context)

@login_required
def Years(request):
    """Shows all years with registered purchases."""
    # Stores all the purchases made by the user.
    purchases = Purchase.objects.filter(owner=request.user).order_by('date_purchase')
    # List to store the years with registered purchases.
    years = []
    for purchase in purchases:
        # Verifies if the year is already stored.
        if purchase.date_purchase.year not in years:
            years.append(purchase.date_purchase.year)
    context = {'years': years}
    return render(request, 'shopping_registry/years.html', context)

@login_required
def Months(request, year):
    """Shows all the months with registered purchases in the selected month."""
    # Stores all the purchases registered by the User.
    purchases = Purchase.objects.filter(owner=request.user).order_by('date_purchase')
    # List to store all the months.
    months = []
    for purchase in purchases:
        # Verifies if the month hasn't been stored yet.
        if purchase.date_purchase.month not in months:
            months.append(purchase.date_purchase.month)
    # Stores the month and year together as a datetime value.
    datetimes = []
    for month in months:
        datetimes.append(datetime.datetime(year, month, 1).date())
    # Find a way to turn the int value to a month datetime.
    context = {'months': months, 'dates': datetimes, 'year': year}
    return render(request, 'shopping_registry/months.html', context)

@login_required
def registering_instructions(request):
    """Page that links to the PurchaseForm and includes instructions."""
    return render(request, 'shopping_registry/instrucciones_registro.html')

@login_required
def new_category(request):
    """Add a new category."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CategoryForm()
    else:
        # POST data submitted; process data.
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect('shopping_registry:new_product')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'shopping_registry/new_category.html', context)

@login_required
def new_purchase(request):
    """Add a new purchase."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PurchaseForm()
    else:
        # POST data submitted; process data.
        form = PurchaseForm(data=request.POST)
        if form.is_valid():
            new_purchase = form.save(commit=False)
            new_purchase.owner = request.user
            new_purchase.save()
            return redirect('shopping_registry:dates')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'shopping_registry/new_purchase.html', context)

@login_required
def new_product(request):
    """Add a new product."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProductForm()
    else:
        # POST data submitted; process data.
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = request.user
            new_product.save()
            return redirect('shopping_registry:new_purchase')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'shopping_registry/new_product.html', context)