"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all purchases.
    path('dates/', views.dates, name="dates"),
    # Detail page for a single purchase.
    path('dates/<int:date_id>/', views.date, name='date'),
    # Page that displays all years with registered purchases.
    path('years/', views.Years, name='years'),
    # Page that displays the months in a year.
    path('<int:year>/', views.Months, name='months'),
    # Detail page for a month's shopping trips.
    # Example: /2021/12/
    path('<int:year>/<int:month>/', views.MonthView, name='MonthView'),
    # Page for adding a new category.
    path('new_category/', views.new_category, name='new_category'),
    # Page for adding a new purchase.
    path('new_purchase/', views.new_purchase, name='new_purchase'),
]