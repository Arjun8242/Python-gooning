# nums = [2,3,4,5,6,7]
# nums[1:4] = [10,12,14]
# print(nums)

# list = [2,3,4,5]
# print(type(list)) #list in square brcket       list is mutable
# list = tuple(list)
# print(type(list)) #tuple in round bracket      tuple is immutable


# tup = (69, 'arjun', 3.14, True)

# num, name, pi, bool = tup

# print(num)
# print(name)
# print(pi)
# print(bool)

#reverse indexing of tuple
# tup = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
# print(tup[-1])
# print(tup[-2])
# print(tup[-3])
# print(tup[-4])
# print(tup[-5])
# print(tup[-6])
# print(tup[-7])
# print(tup[-8])
# print(tup[-9])
# print(tup[-10])

#slice index  (start:stop:step)        
# print(tup[0:5])

#you can change the list inside of tuple
# tup = (1, 2, [3, 4, 5])
# tup[2][0] = 10
# print(tup)


#set
# set = {1, 2, 3, 4, 5}
# set.add(6)
# print(set)

#dictionaries
# data = {
#     "name" : "Arjun",
#     "age" : 21,
#     "gender" : "Male",
#     "city" : "varanasi"
# }
# print(data.values()) #this will print the values of the dictionary
# print(data.keys()) #this will print the keys of the dictionary
# print(data.items()) #this will print the items of the dictionary
# print(data["name"]) #this will print the value of the key name


#everything in python is object

# a=5
# print(id(a))    #memory location
# print(type(a))  #type of object
# print(a.__class__) #class of object    

# a, b = 8, 4
# print(a>10 and b<10)

# print(a>10 or b<10)

# print(not(a>10 and b<10))  

# def add(x, y):
#     a=x
#     b=y
#     c=a+b
#     return c

# print(add(3,4))

# import math

# print(math.sqrt(16))  


#swapping 

#first method
# a, b = 10, 20
# a,b = b,a  tuple packing and tuple unpacking
# print(a)
# print(b)

#second method
# x, y = 10, 20
# x = x^y
# y = y^x
# x = x^y
# print(x)
# print(y)

#3rd method
# x, y = 10, 30
# x = x*y
# y = x//y
# x = x//y
# print(x)
# print(y)

# a = input()
# b = input()

# a, b = b, a
# print(a+b)


# a=input()
# match a:
#     case '1':
#         print("one")
#     case '2':
#         print("two")
#     case '3':
#         print("three")
#     case '4':
#         print("four")
#     case '5':
#         print("five")
#     case '6':
#         print("six")
#     case '7':
#         print("seven")
#     case '8':
#         print("eight")
#     case '9':
#         print("nine")
#     case '10':
#         print("ten")
#     case _:
#         print("invalid input")   

# tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


# for value in tuple:
#     print(value)

# import os
# curr_dir=os.getcwd()
# print(curr_dir)

import json
data = {
    "name" : "Arjun",
    "age" : 21,
    "gender" : "Male",
    "city" : "varanasi"
}

with open("data.json", "w") as f:
    json.dump(data, f)

# pip freeze > requirments.txt adds requirments.txt file 