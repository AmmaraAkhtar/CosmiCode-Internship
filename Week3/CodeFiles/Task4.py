def Palindrome(s):
    clean_str=''.join(s.split()).lower()
    return clean_str==clean_str[::-1 ]

s=input("Enter the Palindrome:")
if Palindrome(s):
    print("The string is Palindrome.")
else:
    print("The string is not Palindrome.")


    
