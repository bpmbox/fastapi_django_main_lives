from src.fraction_operations import FractionOperations
import pytest

def test_add_fractions():
    fraction_operations = FractionOperations()
    fraction1 = Fraction(1, 2)
    fraction2 = Fraction(1, 3)
    result = fraction_operations.add_fractions(fraction1, fraction2)
    assert result == Fraction(5, 6)

def test_divide_by_zero():
    fraction_operations = FractionOperations()
    fraction1 = Fraction(1, 2)
    fraction2 = Fraction(0, 1)
    result = fraction_operations.divide_fractions(fraction1, fraction2)
    assert result is None
    assert fraction_operations.get_errors() == ["Error: Division by zero is not allowed"]