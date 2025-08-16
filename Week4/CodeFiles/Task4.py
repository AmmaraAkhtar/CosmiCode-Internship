def Chracter_fre(text):
    fre={}
    for char in text:
        if char in fre:
            fre[char] +=1
        else:
            fre[char]=1

    return fre


text="Ammara Akhtar"
res=Chracter_fre(text)

for char, count in res.items():
    print(f'{char}: {count}')