from .models import Purchase

def calculate_total(purchases):
    """Calculates the total spent for the given purchases and 
        rounds the result."""
    total = 0

    for purchase in purchases:
        total += purchase.price

    total = round(total, 2)
    
    return total

def total_categories(purchases):
    """Calculates the total spent per category for the given purchases."""
    categories_total = {}

    for purchase in purchases:
        if purchase.category.title() not in categories_total:
            categories_total[purchase.category.title()] = 0
            categories_total[purchase.category.title()] += purchase.price
        else:
            categories_total[purchase.category.title()] += purchase.price

    return categories_total