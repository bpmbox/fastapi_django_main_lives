from .fraction_operations import FractionOperations

def main():
    fraction_operations = FractionOperations()

    fraction1 = Fraction(1, 2)
    fraction2 = Fraction(1, 3)

    result = fraction_operations.add_fractions(fraction1, fraction2)
    if result:
        print("Result:", result)
    else:
        print("Errors:", fraction_operations.get_errors())

    result = fraction_operations.divide_fractions(fraction1, Fraction(0, 1))
    if result:
        print("Result:", result)
    else:
        print("Errors:", fraction_operations.get_errors())

if __name__ == "__main__":
    main()