def seconds_to_string(seconds):
    periods = [
        ('d', 60 * 60 * 24),
        ('h', 60 * 60),
        ('m', 60),
        ('s', 1)
    ]

    for unit, period_seconds in periods:
        if seconds >= period_seconds:
            return str(int(divmod(seconds, period_seconds)[0])) + unit
