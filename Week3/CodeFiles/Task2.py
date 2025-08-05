def Reversed(arr):
    
    reversed_arr=[]
    for i in range(len(arr)-1,-1,-1):
        reversed_arr.append(arr[i])
        
    return reversed_arr 
    

arr=[1,5,6,7,3,4]
reversed=Reversed(arr)
print("Original Array:",arr)
print("Reversed Array:",reversed)
