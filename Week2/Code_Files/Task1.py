def is_prime(n):
    count=0
    for i in range(1,n+1):
        if n%i==0:
            count +=1
    if count==2:
        return True
    else:
        return False
    

num=int(input("Enter the number:"))
if is_prime(num):
    print ("The Entered number is Prime")
else:
    print("The entered number is not prime")

print("|---The list of prime number up to entered number---|")
for i in range(1,num+1):
    if is_prime(i):
        print(i,end=" ")
    else:
        continue