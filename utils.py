MIN_TEMP: float = -273.15

number = int | float

def clamp(self, n: number, lower: number=float("inf"),
           upper: number=float("inf")) -> number:
    return max(lower, min(n, upper))