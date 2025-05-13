def divide_by_two(number):
    try:
        return number / 2
    except TypeError:
        raise ValueError("ورودی باید یک عدد باشد.")
