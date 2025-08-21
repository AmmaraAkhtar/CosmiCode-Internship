import math
class shape:
    def area():
        pass
    def perimeter():
        pass

class circle(shape):
    def __init__(self,r):
        self.r=r
    def area(self):
        print(f"The area of circle is: {math.pi*self.r*self.r}" )
    def perimeter(self):
        print(f"The Perimeter of Circle is: {2*math.pi*self.r}\n")

class rectangle(shape):
    def __init__(self,l,w):
        self.l=l
        self.w=w
    def area(self):
        print(f"The area of rectangle is: {self.l*self.w}" )
    def perimeter(self):
        print(f"The Perimeter of rectangle is: {2*self.l*self.w}\n")

    


class Triangle(shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        print(f"The area of Triangle is: {math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))}" )

    def perimeter(self):
         print(f"The Perimeter of Triangle is: {self.a + self.b + self.c}\n")


c=circle(12)
c.area()
c.perimeter()


r=rectangle(12,5)
r.area()
r.perimeter()

t=Triangle(2,3,4)
t.area()
t.perimeter()
