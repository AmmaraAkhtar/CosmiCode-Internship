class complex:
    def __init__(self, real,img):
        self.real=real
        self.img=img

    def __str__(self):
        return f"{self.real}+{self.img}i"
    
    def __add__(self,other):
        return complex(self.real+other.real, self.img+self.img)
    
    def __sub__(self,other):
        return complex(self.real-other.real, self.img-self.img)
    
    def __mul__(self,other):
        real=(self.real*other.real)-(self.img*other.img)
        img=(self.real*other.img)+(self.img*other.real)
        return complex(real,img)
    
    def __truediv__(self,other):
        deno=(other.real*other.real)+(other.img*other.img)
        real=((self.real*other.real)+(self.img*other.img))/ deno
        img=((other.real*other.img)-(self.real*self.img))/deno
        return complex(real,img)


c1=complex(2,3)
c2=complex(6,7)

print("C1=",c1)
print("C2=",c2)
print("C1+C2:",c1+c2)
print("C1-C2:",c1-c2)
print("C1*C2:",c1*c2)
print("C1/C2:",c1/c2)