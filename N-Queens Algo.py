def dfs_n_queens(n: int):


    output = []
    if n < 1:
        return output
    elif n == 1:
        return [[0]]

    output = []



    queens = []
    
        
    def safe(row, column, queens):
        for queen in queens:
            old_row, old_column = queen
            if column == old_column:
                return False
            elif abs(old_row - row) == abs(old_column - column):
                return False
            
        return True

    def DFS(row):
        solution = []
        if row == n:
            for queen in queens:
                row, column = queen
                solution.append(column)
            output.append(solution)
            return
        for column in range(n):
            if safe(row, column, queens):
                queens.append((row, column))
                result = DFS(row + 1)
                
                queens.pop()

    final_output = ""
    for row in output:
        for character in row:
            final_output += character
        final_output += "\n"
    
    print(final_output)
    DFS(0)
    return output
        

    

print(dfs_n_queens(5))
