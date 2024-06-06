
print()
print("This is  Our List")

Num_list= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,]

list2= [21,22,23,]


Num_list.sort()

print(Num_list)

print()
print("Added An Other Three Numbers In The List") 

new_list = Num_list + list2

print (new_list)





print()
print("Five Largest Number In The List")  


print(new_list[18:23])

print()
print("Three Smallest Number In A List") 

print(Num_list[0:3])


print()
print("Deleted Even Numbers") 

for i in new_list:
    if i % 2 == 0:
       new_list.remove(i)
print(new_list)
    



   

print()
print("Deleted Odd Numbers Less Than 9") 

for i in  range (9):
    if i %2 != 0:
       new_list.remove(i)
print(new_list)
    



   














