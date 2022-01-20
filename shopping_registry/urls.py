"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that displays instructions and links to the new_product view.
    path('instructions/', views.registering_instructions, name='registering_instructions'),
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
    path('registrar_categoria/', views.new_category, name='new_category'),
    # Page for adding a new purchase.
    path('registrar_compra/', views.new_purchase, name='new_purchase'),
    # Page for adding a new product.
    path('registrar_producto/', views.new_product, name='new_product'),
    # Page for adding a new date.
    path('registrar_fecha/', views.new_date, name='new_date'),
]