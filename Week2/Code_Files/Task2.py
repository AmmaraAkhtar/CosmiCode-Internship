# iterative approach
print("|Iterative Approach|")
def iterative_approach(n):
    a,b=0,1
    fibonacci_series=[]
    for i in range(n):
        fibonacci_series.append(a)
        a,b=b,a+b

    return fibonacci_series

n=int(input("Enter the number:"))
print(iterative_approach(n))





#recursive approach
print("|Recursive Approach|")
def recursive(n):
    if n<=1:
        return n

    else:
        return recursive(n-1)+recursive(n-2)
    

n=int(input("Enter the number:"))
for i in range(n):
    print(recursive(i),end=" ")