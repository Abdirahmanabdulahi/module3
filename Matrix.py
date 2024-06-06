
print("1. Add matrix")
print("2. Sub matrix")
print("3. Mult matrix")

print()
print()


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
print()


def Add_Matrix(matrix1, matrix2):
    for i in range(3):
        for j in range(3):
            matrix3 = matrix1[i][j] + matrix2[i][j]
            print(matrix3, end="\t")
        print()

    



def Sub_Matrix(matrix1, matrix2):
    for i in range(3):
        for j in range(3):
            matrix3 = matrix1[i][j] - matrix2[i][j]
            print(matrix3, end="\t")
        print()





def Multiply_Matrix(matrix1, matrix2):
    for i in range(len (matrix1) ):
        for j in range(len (matrix2[0]) ):
            for k in range(len (matrix2)):
                matrix3[i][j] += matrix1[i][k] * matrix2[k][j]

    for m in matrix3:
        print(m)        

        
choice = input("Choose an option: ")
if choice == "1":
    print("Display Add Matrix")
    Add_Matrix(matrix1,matrix2)

elif choice == "2":
    print("Display Subtract Matrix")
    Sub_Matrix(matrix1, matrix2)

elif choice == "3":
    print("Display Multiply Matrix")
    Multiply_Matrix(matrix1, matrix2)
    
else:
    print("Sorry, this is invalid option Please try again ")











    
