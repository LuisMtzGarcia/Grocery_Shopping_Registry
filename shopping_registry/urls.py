"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that displays instructions and links to the new_product view.
    path('instructions/', views.registering_instructions, 
        name='registering_instructions'),
    # Page that shows all purchases.
    path('dates/', views.dates, name="dates"),
    # Detail page for a single date.
    path('dates/<int:date_id>/', views.date, name='date'),
    # Page for editing a date.
    path('editar/fecha/<int:date_id>', views.edit_date, name='edit_date'),
    # Page for editing a purchase.
    path('editar/compra/<int:purchase_id>', views.edit_purchase, name='edit_purchase'),
    # Page for editing a category.
    path('editar/categoria/<int:category_id>', views.edit_category, name='edit_category'),
    # Page to confirm the deletion of a single date.
    path('borrar/confirmar/<int:date_id>', views.erase_date_confirmation, name='erase_date_confirmation'),
    # Page for deleting a single date.
    path('borrar/fecha/<int:date_id>', views.erase_date, name='erase_date'),
    # Page for editing a purchase.
    # Falta terminar esto
    #path('editar/compra/<int:compra_id>', views.edit_purchase, name='edit_purchase'),
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
    # Pasar la id de la fecha o compra o etc a otra view dentro de la view
]