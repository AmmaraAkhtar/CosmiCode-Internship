def find_Target(list, target):
    left=list[0]
    right=len(list)-1

    if left<=right:
        mid=(left+right)//2
        if list[mid]==target:
            return mid
        elif list[mid]<target:
            left=mid+1
        elif list[mid]>target:
            right=mid-1
        else:
            return -1
        

arr=[2,4,6,8,10,12]
pos=find_Target(arr, 8)
if  pos!=-1:
    print(f"Target found at index {pos}")
else:
    print("Target not Found")
