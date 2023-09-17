#!/usr/bin/env python3


def factorial(x):
    """
    calculating the factorial of a non-negative integer

    Args:
        x(int): the non-negative integr for which the factorail is calculated

    Returns:
        int: the factorial of the integer inputed

    Raises:
        ValueError: if the inputed integer is a negative number
    """
    if x < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if x == 0:
        return 1
    result = 1

    for i in range(1, x + 1):
        result *= i
    return result


def main():
    """main function to get user input and calculate factorial"""
    try:
        num = int(input("Enter a non-negative integer:"))
        result = factorial(num)
        print(f"The factorial of {num} is {result}")
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation aborted by user.")


if __name__ == "__main__":
    main()
