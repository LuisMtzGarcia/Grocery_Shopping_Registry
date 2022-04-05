from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from shopping_registry.models import Purchase

import datetime

User = get_user_model()

class PurchaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods.
        Purchase.objects.create(
            product='queso', 
            category='comida',
            quantity=200,
            price=21.90,
            date_purchase=datetime.date(2022, 2, 18),
            bulk=True,
            owner=User.objects.create()
            )

    def test_product_label(self):
        purchase = Purchase.objects.get(id=1)
        field_label = purchase._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_category_label(self):
        purchase = Purchase.objects.get(id=1)
        field_label = purchase._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_quantity_label(self):
        purchase = Purchase.objects.get(id=1)
        field_label = purchase._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'quantity')
