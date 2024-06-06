
print()
print("Display Matrix Lists With Out Funcation ")


matrix1 = [
           [12,  10, 0],
           [4 ,  5 , 7],
           [0 ,  6 , 5]

           ]

matrix2 = [
           [9 ,  1 , 9],
           [7 ,  2,  3],
           [8 ,  5 , 0]

           ]

matrix3 = [
           [0 ,  0 , 0],
           [0 ,  0,  0],
           [0 ,  0 , 0]

           ]

print(matrix1)
print(matrix2)


print()
print("Matrix Addition")



for i in range(3):
    for j in range(3):
        matrix3=matrix1[i][j] + matrix2[i][j]
        print(matrix3 , end="\t")
    print()


print()
print("Matrix Subtraction")
  
for i in range(3):
    for j in range(3):
        matrix3=matrix1[i][j] - matrix2[i][j]
        print(matrix3 , end="\t")
    print()




    print()
print("Matrix Multiply")
  

matrix3 = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
for i in range(len (matrix1) ):
    for j in range(len (matrix2[0]) ):
        for k in range(len (matrix2)):
            matrix3[i][j] += matrix1[i][k] * matrix2[k][j]
for m in matrix3 :
    print(m)



    




