def compute_gcd(a,b):
    def gcd(x,y):
        while y!=0:
            x,y=y,x%y
        return x
    gcd_res=gcd(a,b)
    lcm_res=(a*b)//   gcd_res
    return gcd_res,lcm_res


n1=int(input("Enter the first number:"))
n2=int(input("Enter the second number:"))

gcd,lcm=compute_gcd(n1,n2)
print(f" Greatest Common Divisor(GCD) is {gcd} ")
print(f" Least Common Multiple (LCM) is {lcm} ")