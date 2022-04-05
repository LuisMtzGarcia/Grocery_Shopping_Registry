from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Purchase(models.Model):
    """The purchase of a product."""
    product = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_purchase = models.DateField()
    # Compras a granel / Bulk purchases
    bulk = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

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