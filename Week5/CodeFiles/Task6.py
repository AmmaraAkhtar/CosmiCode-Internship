class Book:
    def __init__(self,title,author):
        self.title=title
        self.author=author

    def __str__(self):
        return f"title: {self.title}, author: {self.author}"
    

class library:
    def __init__(self):
        self.books=[]
    def add(self,book):
        self.books.append(book)
        print("{book.title} are aadded successfully")
        
    def remove(self,title):
        for book in self.books:
            if book.title==title:
                self.books.remove(book)
                print(f"Book {title} remove successfully")
                return
        print(f"Book {title} are found in libraray")
    def display(self):
        for book in self.books:
            print(f"- {book.title}")



b1=Book("1234","Programming")
b2=Book("1235","C++")
b3=Book("1236","C#")
b4=Book("1237","Java")



v=library()

v.add(b1)

v.add(b2)

v.add(b3)

v.add(b4)
print("Books Before Removing")
v.display()
print()
v.remove("1236")

print()
print("Books After Removing")
v.display()
