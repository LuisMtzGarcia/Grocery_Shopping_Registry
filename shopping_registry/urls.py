"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that displays instructions and links to the new_product view.
    path('instrucciones/registro', views.registering_instructions, 
        name='registering_instructions'),
    # Page that displays instructions for the use of the demo account.
    path('instrucciones/demo', views.demo_account_instructions, 
        name='demo_instructions'),
    # Page that shows all purchases.
    path('dates/', views.dates, name="dates"),
    # Detail page for a single date.
    path(r'dates/(<date>\d{4}-\d{2}-\d{2})/', views.date, name='date'),
    # Page for adding a new purchase.
    path('registrar_compra/', views.new_purchase, name='new_purchase'),
    # Page for editing a purchase.
    path('editar/compra/<int:purchase_id>', views.edit_purchase, 
        name='edit_purchase'),
    # Page to confirm the deletion of a single date.
    path(r'confirmar/borrar/(<date_string>\d{4}-\d{2}-\d{2})/', views.erase_date_confirmation, 
        name='erase_date_confirmation'),
    # Page to confirm the deletion of a single purchase.
    path('confirmar/compra/<int:purchase_id>', views.delete_purchase_confirmation, 
        name='delete_purchase_confirmation'),
    # Page for deleting all the purchases made on the selected date.
    path(r'borrar/(<date_string>\d{4}-\d{2}-\d{2})/', views.erase_date, name='erase_date'),
    # Page for deleting a single purchase.
    path('borrar/compra/<int:purchase_id>', views.delete_purchase, 
        name='delete_purchase'),
    # Page that displays all years with registered purchases.
    path('years/', views.Years, name='years'),
    # Page that displays the months in a year.
    path('<int:year>/', views.Months, name='months'),
    # Detail page for a month's shopping trips.
    # Example: /2021/12/
    path('<int:year>/<int:month>/', views.MonthView, name='MonthView'),
]