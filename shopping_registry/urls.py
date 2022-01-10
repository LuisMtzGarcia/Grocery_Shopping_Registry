"""Defines URL patters for Grocery Registry"""

from django.urls import path

from . import views
from shopping_registry.views import YearView, MonthView

app_name = 'shopping_registry'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all purchases.
    path('dates/', views.dates, name="dates"),
    # Detail page for a single purchase.
    path('dates/<int:date_id>/', views.date, name='date'),
    # Page that shows all months in a year.
    path('<int:year>/', YearView.as_view(), name="date_archive_year"),
    # Page that shows all shopping trips in a year.
    # Example: /2021/12/
    path('<int:year>/<int:month>/', MonthView.as_view(month_format='%m'),
        name="archive_month_numeric"),
    # Example: /2021/dec/
    path('<int:year>/<str:month>/', MonthView.as_view(), name="archive_month"), 
]