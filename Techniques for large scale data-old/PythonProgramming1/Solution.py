import argparse

def fib(limit):
    # Given an input limit, calculate the Fibonacci series within [0,limit]
    i = 0
    a = 0
    b = 1
    while i<limit:
        yield b
        b = a+b
        a = b-a
        i += 1
        
def list_fib(limit):
    # Construct a list of Fibonacci series
    fibonacci_series = [0]
    for i in fib(limit):
        fibonacci_series.append(i)
    return fibonacci_series


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the fibonacci sequence up to a specified limit (n)")
    parser.add_argument("limit", type=int, help="A limit for the sequence")
    args = parser.parse_args()
    print(list_fib(args.limit))

