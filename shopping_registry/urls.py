"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all purchases
    path('dates/', views.dates, name="dates"),
    # Detail page for a single purchase
    path('dates/<int:date_id>/', views.date, name='date'),
]