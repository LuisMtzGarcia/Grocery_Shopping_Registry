from django.shortcuts import render
from django.db.models import Sum
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
    # View to calculate the total spent on that trip
    #total_price = purchases.objects.all()
    context = {'date': date, 'purchases': purchases}
    return render(request, 'shopping_registry/date.html', context)
