#  Task 3: Write a program that takes user input for three numbers
#  and prints the largest and smallest among them.


a=int(input("Enter the First Number:"))
b=int(input("Enter the Second Number:"))
c=int(input("Enter the Third Number:"))

# prints the largest
if (a>b and a>c):
    print(f"{a} is the Largest Number")
elif (b>a and b>c):
    print(f"{b} is the Largest Number")
else:
    print(f"{c} is the Largest Number")

# prints the smallest
if (a<b and a<c):
    print(f"{a} is the Smallest Number")
elif (b<a and b<c):
    print(f"{b} is the Smallest Number")
else:
    print(f"{c} is the Smallest Number")
