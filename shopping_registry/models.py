from django.db import models

class Category(models.Model):
    """Categories to classify the items."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a string representation of the name of the category."""
        return f"{self.name}"

class Product(models.Model):
    """A product the user pruchases and registers."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        """Return the name of the product in a string."""
        return f"{self.name}"

class Date(models.Model):
    """The purchase date of a group of products in a trip to the supermarket."""
    date_trip = models.DateField()

    class Meta:
        verbose_name_plural = 'dates'

    def __str__(self):
        """Return a string representation of the date."""
        return f"{self.date_trip}"


class Purchase(models.Model):
    """The purchase of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_purchase = models.ForeignKey(Date, on_delete=models.CASCADE)
    # Compras a granel
    bulk = models.BooleanField()

    class Meta:
        verbose_name_plural = 'purchases'

    def __str__(self):
        """Return a string representation of the purchase."""
        if self.bulk == True:
            return f"{self.quantity} gramos de {self.product} por ${self.price}"
        else:
            return f"{self.quantity} de {self.product} por ${self.price}"