def longest_sentance(sentance):
    clean_sentance=""
    for char in sentance:
        if char.isalnum() or  char.isspace():
            clean_sentance += char
    words= clean_sentance.split()
    longest=""
    for word in words:
        if len(word)>len(longest):
            longest=word

    return longest


sen=input("Enter the Sentance:")
print("Sentance:",sen)
print("Longest Sentance:",longest_sentance(sen))

    


