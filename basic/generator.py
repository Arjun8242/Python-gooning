#normal func

def numbers():
    return list(range(5))

print(numbers())


#generator func

def gen_numbers():
    print("Generator started")

    for i in range(3):
        print(f"Before yield: {i}")
        yield i
        print(f"After yield: {i}")

print("Creating generator...")
gen = gen_numbers()

print("First next()")
print(next(gen))

print("Second next()")
print(next(gen))

print("Third next()")
print(next(gen))
