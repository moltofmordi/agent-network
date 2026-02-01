"""
Calculator Module

This module provides a Calculator class with static methods for basic arithmetic operations.
All methods validate inputs and handle edge cases appropriately.
"""


class Calculator:
    """
    A calculator class providing basic arithmetic operations.
    All methods are static and handle input validation.
    """

    @staticmethod
    def add(a, b):
        """
        Add two numbers together.

        Args:
            a: First number (int or float)
            b: Second number (int or float)

        Returns:
            The sum of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Both arguments must be numeric (int or float)")
        return a + b

    @staticmethod
    def subtract(a, b):
        """
        Subtract b from a.

        Args:
            a: Number to subtract from (int or float)
            b: Number to subtract (int or float)

        Returns:
            The difference of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int or float)):
            raise TypeError("Both arguments must be numeric (int or float)")
        return a - b

    @staticmethod
    def multiply(a, b):
        """
        Multiply two numbers.

        Args:
            a: First number (int or float)
            b: Second number (int or float)

        Returns:
            The product of a and b

        Raises:
            TypeError: If inputs are not numeric
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int or float)):
            raise TypeError("Both arguments must be numeric (int or float)")
        return a * b

    @staticmethod
    def divide(a, b):
        """
        Divide a by b.

        Args:
            a: Numerator (int or float)
            b: Denominator (int or float)

        Returns:
            The quotient of a divided by b

        Raises:
            TypeError: If inputs are not numeric
            ZeroDivisionError: If b is zero
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int or float)):
            raise TypeError("Both arguments must be numeric (int or float)")
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
