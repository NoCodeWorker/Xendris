def calculate_discount(price, discount_percent):
    """Apply a discount percentage to a price.

    Returns the discounted price.
    Raises ValueError for invalid inputs.
    Discounts over 100% return 0.
    """
    if price < 0 or discount_percent < 0:
        raise ValueError("price and discount_percent must be non-negative")
    result = price * (1 - discount_percent / 100)
    return max(0, result)
