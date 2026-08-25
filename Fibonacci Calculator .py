def fibonacci(n):
    sequence = [0,1]

    sequence[1] = 1
    if not isinstance(n, int) and n < 0:
        return "This must be a positive integer"
    
    if n == 0:
        return sequence[n]
    if n == 1:
        return 1
    if n >= 2:
        
        for i in range(1, n + 1):
            sequence.append(sequence[i] + sequence[i - 1])
    return(sequence[n])

print(fibonacci(10))

# 0,1,1,2,3,5,8, 
