from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
    """Categories to classify the items."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a string representation of the name of the category."""
        return f"{self.name}"

class Product(models.Model):
    """A product the user pruchases and registers."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        """Return the name of the product in a string."""
        return f"{self.name}"


class Purchase(models.Model):
    """The purchase of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_purchase = models.DateField()
    # Compras a granel / Bulk purchases
    bulk = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'purchases'

    def __str__(self):
        """Return a string representation of the purchase."""
        if self.bulk == True:
            if self.quantity >= 1000:
                return f"{(self.quantity / 1000)} kilo/s de {self.product} por ${self.price}"
            else:
                return f"{self.quantity} gramos de {self.product} por ${self.price}"
        else:
            return f"{self.quantity} de {self.product} por ${self.price}"