#python has type hints which help to provide types to variables and function
#but python doesn't enforces them

def add(a: int, b: int) -> int:
    return a + b

print(add(10, 20))
print(add("hello", "world"))