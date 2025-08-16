def matrix_mulitiplication(a,b):
    row_a=len(a)
    col_a=len(a[0])
    row_b=len(b)
    col_b=len(b[0])


    if col_a!=row_b:
        print("Matrix Multiplicatin Not Possible..")
        return None
    
    result =[]
    for i in range(row_a):
        row=[]
        for j in range (col_b):
            row.append(0)
        result.append(row)

    for i in range(row_a):
        for j in range(col_b):
            for k in range(col_a):
                result[i][j] += a[i][k]*b[k][j]
    return result



a= [
    [1, 2, 3],
    [4, 5, 6]
]

b = [
    [7, 8],
    [9, 10],
    [11, 12]
]
result=matrix_mulitiplication(a,b)
if result:
    print("Resultant Matrix")
    for row in result :
        print (row)