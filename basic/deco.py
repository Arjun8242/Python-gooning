#A decorator

#adds extra behavior to a function without changing the function itself.


def greater_first(func):
    def wrapper(a,b):
        print("Calling function...")
        if a < b:
            a, b = b, a
        result = func(a,b)
        print("Function called!")
        return result
    return wrapper



@greater_first
def divide(a,b):
    return a/b

@greater_first
def sub(a,b):
    return a-b


result = divide(2, 10)
print("divide result :", result)

result = sub(10,2)
print("sub result :", result)

