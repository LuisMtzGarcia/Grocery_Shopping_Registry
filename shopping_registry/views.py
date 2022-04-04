from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core import serializers
from django.db.models import Sum

from shopping_registry import accountVerification
from shopping_registry import totalCalculations

from .models import Purchase
from .forms import PurchaseForm

import plotly.graph_objects as go

import json
import datetime

def generatePieGraph(categories_total):
    """Generates a pie graph displaying the total spent per category."""

    # Stores keys and values from dict to use as labels and values in the charts.
    # Pie graph.
    pie_labels = categories_total.keys()
    pie_values = categories_total.values()

    # Casts into list for graph compatibility.
    # Pie graph.
    pie_labels = list(pie_labels)
    pie_values = list(pie_values)

    # Pie graph.
    Pie = go.Pie(labels=pie_labels, values=pie_values, hole=.3, 
        title_text="Categorias")
    pie_chart = go.Figure(data=Pie)
    pie_graph = pie_chart.to_html()

    return pie_graph

def generateBarGraph(x, y):
    """Generates a pie graph displaying the total spent per product."""

    Bar = go.Bar(x=x, y=y)
    layout = go.Layout(title="Productos y costo", xaxis={'title':'Productos'}, 
        yaxis={'title':'Costo'})
    figure = go.Figure(data=[Bar],layout=layout)
    bar_graph = figure.to_html()  

    return bar_graph  

def index(request):
    """The home page for Registro-Super."""
    return render(request, 'shopping_registry/index.html')

@login_required
def dates(request):
    """Shows all dates."""
    dates = []

    purchases = Purchase.objects.filter(owner=request.user).order_by('-date_purchase')

    for purchase in purchases:
        if purchase.date_purchase not in dates:
            dates.append(purchase.date_purchase)

    context = {'dates': dates}
    return render(request, 'shopping_registry/dates.html', context)

@login_required
def date(request, date):
    """Shows all the information for a day's purchases."""
    
    date_string = date
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    purchases = Purchase.objects.filter(date_purchase=date, owner=request.user)

    total = totalCalculations.calculate_total(purchases)

    products = []

    quantities = []

    prices = []

    ind_prices = [] 

    # Stores the name of the product, its individual price and its bulk's boolean
    # value
    dictionary = {}

    categories = []

    categories_total = totalCalculations.total_categories(purchases)

    bulk = []

    for purchase in purchases:
        products.append(purchase.product)
        quantities.append(purchase.quantity)
        prices.append(purchase.price)
        bulk.append(purchase.bulk)

    for x in range(0, len(products)):
        if purchases[x].category.title() not in categories:
            categories.append(purchases[x].category.title())

        if bulk[x] == True:
            # If it was a bulk purchase, multiply by 100 to display the price per
            # 100 grams.
            ind_prices.append(float((prices[x] / quantities[x]) * 100))
        else:
            ind_prices.append(float((prices[x] / quantities[x])))

        ind_prices[x] = round(ind_prices[x], 2)

        dictionary[x] = {'Nombre': purchases[x], 'Categoria': purchases[x].category,
            'Bulk': bulk[x], 'Precio': ind_prices[x]}


    # Product and Price visualization

    # Convert the prices list QuerySet to a list of floats.
    prices_float = [float(price) for price in prices]

    # Generating the charts.
    # Bar chart.
    bar_graph = generateBarGraph(products, prices_float)

    # Pie chart.
    pie_graph = generatePieGraph(categories_total)

    context = {'date': date, 'date_string': date_string, 'purchases': purchases, 'total':total, 
        'products':products, 'ind_prices':ind_prices, 'dictionary': dictionary,
        'categories': categories, 'categories_total': categories_total, 
        'bar_graph': bar_graph, 'pie_graph': pie_graph}
    return render(request, 'shopping_registry/date.html', context)

@login_required
def edit_purchase(request, purchase_id):
    """Edit an existing purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # Checks if user is using demo account and is the owner of the object.
    accountVerification.check_account(request.user.username, purchase)

    date = purchase.date_purchase

    # Passes the data to the form template.
    formatedDate = date.strftime("%m/%d/%Y")

    initial_dict = {
        "date_purchase" : formatedDate,
        "bulk": True,
    }

    if request.method != 'POST':
        # Initial request; pre-fill form with the current purchase.
        form = PurchaseForm(instance=purchase, initial=initial_dict)
    else:
        # POST data submitted; process data.
        form = PurchaseForm(data=request.POST, instance=purchase)

        if form.is_valid():
            edited_purchase = form.save(commit=False)
            edited_purchase.owner = request.user
            edited_purchase.save()
            return redirect('shopping_registry:date', date=date)

    context = {'purchase': purchase, 'form': form, 'date': formatedDate}
    return render(request, 'shopping_registry/edit_purchase.html', context)

@login_required
def erase_date_confirmation(request, date_string):
    """Confirm the deletion of the purchases done on the selected date."""

    accountVerification.check_account(request.user.username)

    purchases = Purchase.objects.filter(date_purchase=date_string, owner=request.user)

    # Date is stored in string 'YYYY-MM-DD', converted to datetime value.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    context = {'date': date, 'purchases': purchases, 'date_string': date_string}
    return render(request, 'shopping_registry/erase_date_confirmation.html', context)

@login_required
def erase_date(request, date_string):
    """Delete all the purchases done on the selected date."""

    accountVerification.check_account(request.user.username)

    # Date_string is stored in string format 'YYYY-MM-DD', 
    # converted to datetime value.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    purchases = Purchase.objects.filter(date_purchase=date_string, owner=request.user)

    purchases_erase = purchases.delete()

    context = {'date': date, 'purchase': purchases}
    return render(request, 'shopping_registry/erase_date.html', context)

@login_required
def delete_purchase_confirmation(request, purchase_id):
    """Confirms the deletion of a purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    accountVerification.check_account(request.user.username, purchase)

    context = {'purchase': purchase}
    return render(request, 'shopping_registry/delete_purchase_confirmation.html', 
        context)    

@login_required
def delete_purchase(request, purchase_id):
    """Deletes a single purchase."""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    accountVerification.check_account(request.user.username, purchase)

    purchase_erase = purchase.delete()

    context = {'purchase': purchase}
    return render(request, 'shopping_registry/delete_purchase.html', context)

@login_required
def MonthView(request, year, month):
    """Displays all shopping trips in a month."""

    purchases = Purchase.objects.filter(date_purchase__year=year, 
        date_purchase__month=month, owner=request.user)

    total = totalCalculations.calculate_total(purchases)

    dates = []

    products_total = {}

    categories_total = totalCalculations.total_categories(purchases)

    for purchase in purchases:
        if purchase.product not in products_total:
            products_total[purchase.product] = 0
            products_total[purchase.product] += purchase.price
        else:
            products_total[purchase.product] += purchase.price

        if purchase.date_purchase not in dates:
            dates.append(purchase.date_purchase)

    date = datetime.datetime(year, month, 1)

    # Stores keys and values from dict to use as labels and values in the charts.
    # Bar chart.
    bar_labels = products_total.keys()
    bar_values = products_total.values()

    # Casts into list for chart compatibility.
    # Bar chart.
    bar_labels = list(bar_labels)
    bar_values = list(bar_values)

    # Generating the charts.
    # Bar chart.
    bar_graph = generateBarGraph(bar_labels, bar_values)

    # Pie chart.
    pie_graph = generatePieGraph(categories_total)

    context = {'date': date, 'dates': dates, 'total':total, 
        'products_total': products_total, 'categories_total': categories_total,
        'bar_graph': bar_graph, 'pie_graph':pie_graph}
    return render(request, 'shopping_registry/month_view.html', context)

@login_required
def Years(request):
    """Shows all years with registered purchases."""

    purchases = Purchase.objects.filter(owner=request.user).order_by('date_purchase')

    years = []
    for purchase in purchases:
        if purchase.date_purchase.year not in years:
            years.append(purchase.date_purchase.year)
    context = {'years': years}
    return render(request, 'shopping_registry/years.html', context)

@login_required
def Months(request, year):
    """Shows all the months with registered purchases in the selected month."""
    purchases = Purchase.objects.filter(owner=request.user).order_by('date_purchase')

    months = []
    for purchase in purchases:
        if purchase.date_purchase.month not in months:
            months.append(purchase.date_purchase.month)

    datetimes = []
    for month in months:
        datetimes.append(datetime.datetime(year, month, 1).date())

    context = {'months': months, 'dates': datetimes, 'year': year}
    return render(request, 'shopping_registry/months.html', context)

@login_required
def registering_instructions(request):
    """Page that links to the PurchaseForm and includes instructions."""

    accountVerification.check_account(request.user.username)

    return render(request, 'shopping_registry/instrucciones_registro.html')

def demo_account_instructions(request):
    """Page that links to the log-in form and includes instructions regarding the
    use of the demo account."""

    return render(request, 'shopping_registry/instrucciones_demostracion.html')

@login_required
def new_purchase(request):
    """Add a new purchase."""
    username = request.user.username
    accountVerification.check_account(username)

    next = redirect('shopping_registry:dates')

    print("this works")

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PurchaseForm()
    else:
        # POST data submitted; process data.
        form = PurchaseForm(data=request.POST)
        if form.is_valid():
            date = form['date_purchase'].value()
            new_purchase = form.save(commit=False)
            new_purchase.owner = request.user
            new_purchase.save()
            # Clears the form incase the user wants to register antoher purchase.
            form = PurchaseForm()
            if 'saveAnother' in request.POST:
                # Find way to store date value in form to display it again.
                next = redirect('shopping_registry:new_purchase')
            return next

    context = {'form': form}
    return render(request, 'shopping_registry/new_purchase.html', context)