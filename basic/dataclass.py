#Without a dataclass

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"

#With a dataclass

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    
# with dataclass we don't have to create this dunder methods

#dunder method or special method

#slots keyword is used to reduce memory usage

# | Method        | Purpose                                     |
# | ------------- | ------------------------------------------- |
# | `__init__`    | Initialize a new object                     |
# | `__repr__`    | Official string representation of an object |
# | `__str__`     | Human-friendly string representation        |
# | `__eq__`      | Define behavior of `==`                     |
# | `__lt__`      | Define behavior of `<`                      |
# | `__len__`     | Define behavior of `len(obj)`               |
# | `__getitem__` | Define behavior of `obj[key]`               |
# | `__iter__`    | Make an object iterable                     |
# | `__call__`    | Make an object callable like a function     |
