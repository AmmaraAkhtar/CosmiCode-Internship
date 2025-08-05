from collections import Counter


with open('task5.txt','r') as file:
    text=file.read()

words=''.join(char.lower() if char.isalnum() or char.isspace() else ' ' for char in text ).split()
word_counts=Counter(words)
most_common=word_counts.most_common(1)[0]

print(f"The most frequent word is '{most_common[0]}' which appears {most_common[1]} times.")