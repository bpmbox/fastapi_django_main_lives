from ifrac import Fraction

class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, error_message):
        self.errors.append(error_message)

    def handle_error(self, error):
        if isinstance(error, ZeroDivisionError):
            self.add_error("Error: Division by zero is not allowed")
        elif isinstance(error, ValueError):
            self.add_error("Error: Invalid input for fraction")
        else:
            self.add_error("Error: Unknown error occurred")

    def get_errors(self):
        return self.errors