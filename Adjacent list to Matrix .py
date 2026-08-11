def adjacency_list_to_matrix(dictionary: dict):


    matrix = [[0] for n in dictionary.keys()]
    for n in range(len(matrix)):
        matrix[n] = [0] * len(matrix)

    for n in dictionary.keys(): #iterate between each key
        for m in dictionary[n]:
            matrix[n][m] = 1


    final_output = ""
    for n in range(len(matrix)):
        final_output += str(matrix[n]) 
        final_output += "\n"

    print(final_output)
    return(matrix) 

adjacency_list_to_matrix({0: [], 1: [], 2: []})





# Turn an adjacent list 
# Create the list, with a list in side for each n in dictionary.keys() 
#   Make the list full of zeros for all n in dictionary.keys

#   Make the value pair the index of the list, vale 2 = index 2 
#   If t
