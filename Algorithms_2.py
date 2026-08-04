# 
# Binary Search and Linear Search
# 

# Linear Search starts at the beginning and iterates through each itme until it finds 
# a target value it is looking for
# 
# If found it returns its index, but if it isnt then it returns -1
# 

# Basic code 

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# O(n) time complexity
# O(1) space complexity 

# Binary Search is more efficient but must be ordered in ascending order
# 
# It divids the list in half and checking if the target value is in the middle of the list
# It will figure if it is in the left or right, divid again and keep on until found
# 
# returns -1 if not there 

# Basic code
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2  

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1   # Sets the low to the right middle, then redos
        else:
            high = mid - 1  # Sets the high to left middle 

    return -1

# We identify a low and high indfex, this is the range the list we are seraching through 
# 
# Time complexity is O(log n)
# Space complexity of binary search is O(1)
# 
# 

# Divide and Conquer and how does Merge Sort work 
# DnC is a technique recursively brealing problems into smaller sub-problems 
#   Key is recursion due to the repeatedly until a base case is reached 
# 
# Basic check 
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    sorted_list = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list

# Time complexity for merge sort would be O(n log n)
# continuously divided in half O(long n) and merged O(m)
#
# it has a psace complexiry of O(n)
# Sorting algorithms like bubble sort useas in place 
# 
# 
# 
#  #



def square_root_bisection(number, tolerance = 0.01, repeat = 5): #Sets a defualt value in function definition 

    if number < 0:
        raise ValueError("Square root of negative number is not defined in real numbers")
    elif number == 0 or number == 1:
        print(f"The square root of {number} is {number}")
        return number
    else:
        if number < 1:
            high = 1
        else:
            high = number 
        low = 0
        range_ = high - low
        for i in range(repeat) + 1:
            range_ = high - low
            if range_ > tolerance and i <= repeat:
                mid = (high + low) / 2
                if mid * mid < number:
                    low = mid
                elif mid * mid > number:
                    high = mid
                else:
                    return mid 
            elif i == repeat and range_ > tolerance: 
        
                print(f"Failed to converge within {repeat} iterations")
                return None
        if mid * mid == (number + tolerance) or mid * mid == (number - tolerance):
            print(f"The square root of {number} is approximately {mid}")
            
    
square_root_bisection(0) == 0
square_root_bisection(1) == 1




def merge_sort(array):
    if len(array) <= 1:
        return
    
    middle_point = len(array) // 2
    left_part = array[:middle_point]
    right_part = array[middle_point:]
    
    merge_sort(left_part)
    merge_sort(right_part)
    
    left_array_index = 0
    right_array_index = 0
    sorted_index = 0
    
    while left_array_index < len(left_part) and right_array_index < len(right_part):
        if left_part[left_array_index] < right_part[right_array_index]:
            array[sorted_index] = left_part[left_array_index]
            left_array_index += 1
        else:
            array[sorted_index] = right_part[right_array_index]
            right_array_index += 1
        sorted_index += 1
    
    while left_array_index < len(left_part):
        array[sorted_index] = left_part[left_array_index]
        left_array_index += 1
        sorted_index += 1
    
    while right_array_index < len(right_part):
        array[sorted_index] = right_part[right_array_index]
        right_array_index += 1
        sorted_index += 1

if __name__ == '__main__':
    numbers = [4, 10, 6, 14, 2, 1, 8, 5]
    print('Unsorted array: ')
    print(numbers)
    merge_sort(numbers)
    print('Sorted array: ')
    print(numbers)    


# bubble sort only looks at ones next to each other 
# 
# 
# 
# 
# 
# # 
