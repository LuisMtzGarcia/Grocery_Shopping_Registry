from django.contrib import admin

from .models import Category, Product, Purchase, Date

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Purchase)

admin.site.register(Date)