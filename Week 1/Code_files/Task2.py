#  Task 2: Create a program to perform advanced arithmetic
#  operations (power, modulo) using functions.

def power(a,b):
    return a**b

def modulo(a,b):
    return a%b


a=int(input("Enter the First Number:"))
b=int(input("Enter the Second Number:"))
print("The Power is :",power(a,b))
print("The Modulo is :",modulo(a,b))