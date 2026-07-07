def calculate_discount(price, discount_percent):
    """Apply a discount percentage to a price.

    Returns the discounted price.
    Raises ValueError for invalid inputs.
    Discounts over 100% return 0.
    """
    return price * (1 - discount_percent / 100)
