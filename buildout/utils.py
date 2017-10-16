def calculate_price(price, level):
    return int(price + 0.999) if level == 1 else calculate_price(3 * price / 2, level - 1)


def calculate_time(price, resources):
    return 3600 * price / resources


def calculate_next_base_price(bases):
    base = [1,2,5][bases%3]
    exponent = int(bases/3)
    return 100*base * 10**exponent
