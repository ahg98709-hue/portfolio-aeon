
import math
from typing import List, Union

# --- Basic Math ---

def add(a: float, b: float) -> float: return a + b
def subtract(a: float, b: float) -> float: return a - b
def multiply(a: float, b: float) -> float: return a * b
def divide(a: float, b: float) -> float: return a / b if b != 0 else 0.0
def power(a: float, b: float) -> float: return a ** b
def sqrt(a: float) -> float: return math.sqrt(a) if a >= 0 else 0.0

# --- Geometry (Area) ---

def area_square(side: float) -> float: return side * side
def area_rectangle(width: float, height: float) -> float: return width * height
def area_circle(radius: float) -> float: return math.pi * radius * radius
def area_triangle(base: float, height: float) -> float: return 0.5 * base * height
def area_parallelogram(base: float, height: float) -> float: return base * height
def area_trapezoid(base1: float, base2: float, height: float) -> float: return 0.5 * (base1 + base2) * height
def area_ellipse(a: float, b: float) -> float: return math.pi * a * b

# --- Geometry (Volume) ---

def volume_cube(side: float) -> float: return side ** 3
def volume_rect_prism(l: float, w: float, h: float) -> float: return l * w * h
def volume_sphere(radius: float) -> float: return (4/3) * math.pi * radius ** 3
def volume_cylinder(radius: float, height: float) -> float: return math.pi * radius * radius * height
def volume_cone(radius: float, height: float) -> float: return (1/3) * math.pi * radius * radius * height

# --- Unit Conversions ---

def c_to_f(c: float) -> float: return (c * 9/5) + 32
def f_to_c(f: float) -> float: return (f - 32) * 5/9
def km_to_miles(km: float) -> float: return km * 0.621371
def miles_to_km(miles: float) -> float: return miles / 0.621371
def kg_to_lbs(kg: float) -> float: return kg * 2.20462
def lbs_to_kg(lbs: float) -> float: return lbs / 2.20462
def m_to_ft(m: float) -> float: return m * 3.28084
def ft_to_m(ft: float) -> float: return ft / 3.28084
def lit_to_gal(lit: float) -> float: return lit * 0.264172
def gal_to_lit(gal: float) -> float: return gal / 0.264172

# --- Statistics ---

def mean(numbers: List[float]) -> float:
    return sum(numbers) / len(numbers) if numbers else 0.0

def median(numbers: List[float]) -> float:
    n = len(numbers)
    if n == 0: return 0.0
    sorted_nums = sorted(numbers)
    if n % 2 == 0:
        return (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    return sorted_nums[n//2]

def mode(numbers: List[float]) -> Union[float, List[float]]:
    if not numbers: return 0.0
    counts = {x: numbers.count(x) for x in set(numbers)}
    max_count = max(counts.values())
    modes = [x for x, count in counts.items() if count == max_count]
    return modes[0] if len(modes) == 1 else modes

def range_stat(numbers: List[float]) -> float:
    return max(numbers) - min(numbers) if numbers else 0.0

def variance(numbers: List[float]) -> float:
    if not numbers: return 0.0
    m = mean(numbers)
    return sum((x - m) ** 2 for x in numbers) / len(numbers)

def stdev(numbers: List[float]) -> float:
    return math.sqrt(variance(numbers))

# --- Number Theory ---

def is_prime(n: int) -> bool:
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def factorial(n: int) -> int:
    return math.factorial(n) if n >= 0 else 0

def fibonacci(n: int) -> List[int]:
    """Generates n fibonacci numbers."""
    if n <= 0: return []
    if n == 1: return [0]
    fibs = [0, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def gcd(a: int, b: int) -> int: return math.gcd(a, b)
def lcm(a: int, b: int) -> int: return (a * b) // math.gcd(a, b) if a and b else 0
