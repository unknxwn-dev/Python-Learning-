def hanoi_solver(disk: int):
    maximum_steps = 2**disk -1
    print(f"Maximum steps allowed is: {maximum_steps}")

    # return string with all the moves taken 
    # Include starting position 
    # Each move on new line 
    # Rods should be a list of int 
    # Seperate each list with a space 


    rod_1 = []
    rod_2 = []
    rod_3 = []

    list_of_disk = list(range(1, disk + 1))
    starting_list = list_of_disk[:: -1]

    
    for i in starting_list:
        rod_1.append(i)

    final_script = [f"{rod_1} {rod_2} {rod_3}\n"]
    

    def mover(source, destination):
        destination.append(source.pop())
        final_script.append(f"{rod_1} {rod_2} {rod_3}\n")
    

    def move_tower(no_of_disks, source, destination, spare):
        if no_of_disks == 1:
            mover(source, destination)
        else: 
            
            move_tower(no_of_disks - 1, source, spare, destination)
            mover(source, destination)
            move_tower(no_of_disks - 1, spare, destination, source )
            
    move_tower(disk, rod_1, rod_3, rod_2)

    final = "".join(final_script)
    return final[:-1]


    


print(hanoi_solver(8))


# To move n disks:
# Move the top n-1 disks out of the way.
# Move the largest disk.
# Move the n-1 disks back.


# for the no in disk 
#  if no - 1 is not 1 then:
#       largest number to last rod
#       
#       spare rod = the empty list rod  
#       move all numbers > the highest number index [0] 
#       to the empty list LOOP, so ... if rod length / 1 ... REPEAT 
#       move the index [0] to the destination rod ( rod_3)
#       To move n disks from source to destination:
