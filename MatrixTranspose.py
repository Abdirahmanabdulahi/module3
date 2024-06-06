print()
print("Matrix List")
matrix = [[12, 4, 0, 9], [10, 5, 6, 1,], [0,7,5,9], [3,5,8,0]]



for row in range(4):
    for col in range(4):
        print(matrix[row][col] , end="\t")
    print( )




print()
print("Matrix Mulipl TWo")

for i in range(4):
    for j in range(4):
        print(matrix[i][j] *2 , end="\t")
    print()




print()
print("Matrix Transpose (Exchange Colmn In to Row)")


for row in range(4):
    for col in range(4):
        print(matrix[col][row] , end="\t")
    print()


