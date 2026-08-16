def dfs(matrix, node):
    visted_node = [node]

    stack = []
    def depth(node_start):
        n = node_start
        for m in range(len(matrix[n])):
            if matrix[n][m] == 1 and m not in visted_node:
                # There is an edfe 
                stack.append(m)
                visted_node.append(m) 
                depth(m)
    depth(node)    
    return visted_node
    



        
print(dfs([[0, 1, 0, 0],
     [1, 0, 1, 0],
     [0, 1, 0, 1], 
     [0, 0, 1, 0]]
     , 1))


print(dfs([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], 3))

# Follow the path untill no more 
#
#           1
#       2       3
#   4               5
#6
# DFS would be 1,2,4,6,3,5 
#
# For loop 
#   recursion, checks for a 1, saves the position
#   
#
