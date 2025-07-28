def max_subarray_sum(arr):
    max_cuurent=max_global=arr[0]
    for i in range(1,len(arr)):
        max_cuurent=max(arr[i],max_cuurent+arr[i])
        max_global=max(max_global,max_cuurent)

    return max_global

arr=[-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Max Subarray Sum is : {max_subarray_sum(arr)}")