
#open
file = open("myfile.txt","r+")
#proccess

data= file.read()
print(data)

print()
print()


def Replace_AndFind():
    find = input("Fadlan geli araygaa radinaysid: ")
    print()
    replace = input("Fadlan geli erayga lagu bedelaa: ")

    print()
    print()

    new = data.replace(find,replace)
    
    print("Mahadsanid waa laguu fuliyay codsigaada")

    print()
    print()
    print(new)
Replace_AndFind()

#close
file.close()





     
