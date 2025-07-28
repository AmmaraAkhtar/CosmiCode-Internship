def prime_factors(n):
    i=2
    factors=[]
    while i*i <=n:
        while n%i==0:
            factors.append(i)
            n //=i
        i +=1

    if n>1:
        factors.append(n)
    return factors 

n=60
print(f"Factors of {n} is {prime_factors(n)}")