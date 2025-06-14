from ifrac import Fraction
from .error_handler import ErrorHandler

class FractionOperations:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def add_fractions(self, fraction1, fraction2):
        try:
            result = fraction1 + fraction2
            return result
        except Exception as e:
            self.error_handler.handle_error(e)
            return None

    def subtract_fractions(self, fraction1, fraction2):
        try:
            result = fraction1 - fraction2
            return result
        except Exception as e:
            self.error_handler.handle_error(e)
            return None

    def multiply_fractions(self, fraction1, fraction2):
        try:
            result = fraction1 * fraction2
            return result
        except Exception as e:
            self.error_handler.handle_error(e)
            return None

    def divide_fractions(self, fraction1, fraction2):
        try:
            result = fraction1 / fraction2
            return result
        except Exception as e:
            self.error_handler.handle_error(e)
            return None

    def get_errors(self):
        return self.error_handler.get_errors()