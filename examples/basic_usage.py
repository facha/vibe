from vibe import code


@code
def greet(name):
    """Returns a friendly greeting for the given name."""


@code
def fib(n):
    """Return the nth Fibonacci number."""


print(greet("Alice"))
print(fib(10))
