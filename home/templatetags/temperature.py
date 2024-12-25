from django.template import Library

register = Library()


@register.filter
def temperature(value: float, rnd: int = 0):
    try:
        prefix = "+" if value > 0 else ""
        value_round = round(value, rnd)
        if value_round == int(value_round):
            value_round = int(value_round)
        return f"{prefix}{value_round}°".replace(".", ",")
    except TypeError:
        return value
