class Animal:
    def speak(self):
        print("Animal speak..")



class dog(Animal):
    def speak(self):
        print("Dog speak..")


class cow(Animal):
    def speak(self):
        print("cow speak..")

a=Animal()
d=dog()
c=cow()

a.speak()
d.speak()
c.speak()