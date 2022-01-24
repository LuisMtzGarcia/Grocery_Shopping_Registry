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
    # Page for adding a new category.
    path('registrar_categoria/', views.new_category, name='new_category'),
    # Page for adding a new purchase.
    path('registrar_compra/', views.new_purchase, name='new_purchase'),
    # Page for adding a new product.
    path('registrar_producto/', views.new_product, name='new_product'),
    # Page for adding a new date.
    path('registrar_fecha/', views.new_date, name='new_date'),
    # Page for editing a date.
    path('editar/fecha/<int:date_id>', views.edit_date, name='edit_date'),
    # Page for editing a purchase.
    path('editar/compra/<int:purchase_id>', views.edit_purchase, 
        name='edit_purchase'),
    # Page for editing a category.
    path('editar/categoria/<int:category_id>', views.edit_category, 
        name='edit_category'),
    # Page for editing a product.
    path('editar/producto/<int:product_id>', views.edit_product, 
        name='edit_product'),
    # Page to confirm the deletion of a single date.
    path('confirmar/fecha/<int:date_id>', views.erase_date_confirmation, 
        name='erase_date_confirmation'),
    # Page to confirm the deletion of a single purchase.
    path('confirmar/compra/<int:purchase_id>', views.delete_purchase_confirmation, 
        name='delete_purchase_confirmation'),
    # Page to confirm the deletion of a single product.
    path('confirmar/producto/<int:product_id>', views.delete_product_confirmation,
        name='delete_product_confirmation'),
    # Page to confirm the deletion of a single category.
    path('confirmar/categoria/<int:category_id>', views.delete_category_confirmation,
        name='delete_category_confirmation'),
    # Page for deleting a single date.
    path('borrar/fecha/<int:date_id>', views.erase_date, name='erase_date'),
    # Page for deleting a single purchase.
    path('borrar/compra/<int:purchase_id>', views.delete_purchase, 
        name='delete_purchase'),
    # Page for deleting a single product.
    path('borrar/producto/<int:product_id>', views.delete_product, 
        name='delete_product'),
    # Page for deleting a single category.
    path('borrar/categoria/<int:category_id>', views.delete_category, 
        name='delete_category'),
    # Page that displays all years with registered purchases.
    path('years/', views.Years, name='years'),
    # Page that displays the months in a year.
    path('<int:year>/', views.Months, name='months'),
    # Detail page for a month's shopping trips.
    # Example: /2021/12/
    path('<int:year>/<int:month>/', views.MonthView, name='MonthView'),
]