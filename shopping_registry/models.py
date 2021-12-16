from django.db import models

class Category:
    """Categories to classify the items."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a string representation of the name of the category."""
        return f"{self.name}"

class Product:
    """A product the user pruchases and registers."""
    name = models.CharField(max_length=100)
    category = modedls.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        """Return the name of the product in a string."""
        return f"{self.name}"

class Purchase:
    """The purchase of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date_purchase = models.DateTimeField(auto_now_add=True)
    # Compras a granel
    bulk = models.BooleanField()

    class Meta:
        verbose_name_plural = 'purchases'

    if self.bulk == True:
        message = f"{self.quantity} gr/ml of {self.product} on {self.date_purchase}"
    else:
        message = f"{self.quantity} of {self.product} on {self.date_purchase}"

    def __str__(self):
        """Return a string representation of the purchase."""
        return f"Bought {self.quantity} {if self.bulk == True }"
