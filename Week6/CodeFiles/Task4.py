from collections import Counter, defaultdict, namedtuple, deque


words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_count = Counter(words)
print("Word Frequency:", word_count)


marks = defaultdict(int)  
marks["Ali"] = 85
marks["Ayesha"] = 90
print("Ali's Marks:", marks["Ali"])
print("Unknown Student Marks:", marks["Unknown"])  


Student = namedtuple("Student", ["name", "age", "grade"])
s1 = Student("Ali", 20, "A")
print("Student Info:", s1.name, s1.age, s1.grade)


dq = deque([1, 2, 3])
dq.append(4)      
dq.appendleft(0)    
print("Deque after append:", dq)
dq.pop()            
dq.popleft()       
print("Deque after pop:", dq)
