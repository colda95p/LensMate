import math
# funzione helper per formattare i valori
def format_value(val):
    if math.isinf(val):
        return "∞"
    elif val < 10:
        return f"{val:.2f}"
    else:
        return f"{round(val)}"