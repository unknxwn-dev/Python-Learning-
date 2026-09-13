#
# I did this to learn to how to optimse certain equations
#







def solution(numbers):
    output = [-1] * len(numbers)
    stack = []

    for i in range(len(numbers)):
        while stack and numbers[i] > numbers[stack[-1]]:
            
            output[stack.pop()] = numbers[i]
        stack.append(i)

    return output




















def solution(numbers):
    output = [-1] * len(numbers)
    stack = []

    for i in range(len(numbers)):
        while stack and numbers[i] > numbers[stack[-1]]:
            output[stack.pop()] = numbers[i]
        stack.append(i)
    return output









def days(prices):
    output = [0] * len(prices)
    stack = []

    for i in range(len(prices)):
        while stack and prices[i] > prices[stack[-1]]:

            old_index = stack.pop()
            output[old_index] = i - old_index
        stack.append(i)
    return output



def checks(sentance):

    stack = []
    string = list(sentance)
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    for i in range(len(sentance)):
        if string[i] in pairs:
            if not stack or stack[-1] != pairs[string[i]]:
                return False
            stack.pop()

        else:
            stack.append(string[i])

    return not stack









def number_line(numbers):
    longest = 1

    numbers_set = set(number)  #Fast check
    for i in numbers:
        if i - 1 not in numbers_set:
            current_length = 1
            while i + 1 in numbers_set:
                current_length += 1
                i = i + 1

            longest = max(longest, current_length)
        return longest




def pair_finder(numbers, target):
    
    pairs = 0 
    seen = {


    }

    for number in numbers:
        aim = target - number
        pairs += seen.get(aim, 0)
        seen[number] = seen.get(number, 0) + 1
    return pairs



    # Start wiht target, run each i in number 
    # store i then check if there is a j, j > i  
    # 
    # 
    # #
            

    


#
# Return the lenght of th elongest substring 
# make a dictionary of the individual keys 

# Why dnt we use nodes ? we cant as it might not be immediately there
#
# Or we can use node, and check if the next letter is the saem as this letter, if not we add to a string then we can return the len of the str 
#  Only thing we need to do is make sure it isnt in there, so we could use a list then .append or .clear
# 
# 
# #


def return_pair(sentance):

    substring = []
    longest_length = 0

    sentance_list = list(sentance)

    for s in range(len(sentance_list)):
        current_letter = sentance_list[s]
        next_letter = sentance_list[s + 1]
        substring.append(current_letter)
        if not current_letter == next_letter and current_letter not in substring:
            substring.append(next_letter)
        if len(substring) > longest_length:
            longest_length = len(substring)
        if current_letter in substring:
            substring.pop(current_letter)
            substring.append(current_letter)



def return_pair(sentance):

    longest_length = 1
    seen = {}
    left = 0 
    
    for s in range(len(sentance)):

        if sentance[s] in seen:
            left = max(seen[sentance[s]] + 1, left)
        
        seen[sentance[s]] = s
        distance = s - left + 1
        if distance >longest_length:
            longest_length = distance

    return longest_length
    



#
# start with empty dictionary 
# set the left = 0 and the right = 0
# enter this into seen = sentance[s] = right 
# add one to right 
# 
# ###


def check_sum(numbers, target):

    numbers_set = set(numbers)
    for number in numbers:
        aim = target - number

        if aim in numbers_set:
            return True
        
    return False



def return_single(numbers):

    seen = {}
    output = []
    for number in numbers:
        seen[number] = seen.get(number, 0) + 1
    
    for n in seen.values():
        if n == 1:
            return n


#
# use a dictionary, for number in numbers
# 
# 
# 
# 
# 
# #



def longest_subarray(numbers, target):
    seen = {0: -1}
    longest = 0 
    running_sum = 0

    for i in range(len(numbers)):
        running_sum += numbers[i]

        aim = running_sum - target

        if aim in seen:
            longest = max(longest, i - seen[aim])
        if running_sum not in seen:
            seen[running_sum] = i

    return longest


def sum_of_subarray(numbers):  #Kadane's algorithm

    largest = numbers[0]
    
    running_sum = 0

    for i in range(len(numbers)):

        running_sum = max(running_sum + numbers[i], numbers[i])
        largest = max(largest, running_sum)
    
    return largest
        



def sum_array_no_dups(numbers):

    longest_chain = 1
    seen = {}

    left = 0

    for i in range(len(numbers)):

        if numbers[i] in seen:
            left = max(left, seen[numbers[i]] + 1)
        
        seen[numbers[i]] = i 

        longest_chain = max(longest_chain, i - left + 1)

    return longest_chain
    


def shortest_highest(numbers, target):

    shortest = len(numbers)
    seen = {}
    left = 0

    for i in range(len(numbers)):
        aim = target - numbers[i]

        if aim in seen:
            shortest = min(shortest, i - seen[aim])

        seen[numbers[i]] = i

    return shortest









def find_indecies(numbers, target):
    seen = {}

    for i in range(len(numbers)):
        if numbers[i] in seen:
            distance = (i - seen[numbers[i]])
            if distance <= target:
                return True
        seen[numbers[i]] = i
    return False





# Use a dictionary, find the same number
#   Check if the abs(i - j) <= k
#       if distance (i - seen[numbers[i]]) < k

# 
# #


def find_no(numbers, target):

    for number in numbers:
        aim = target - number
        if aim in numbers:
            return True 
    return False

# 

def find_dupe(numbers):

    seen = set()
    for number in numbers:
        if number in seen:
            return number
        seen.add(number)
    return None
# 

def two_sum(numbers, target):

    seen = {}
    output = []

    for i in range(len(numbers)):
        aim = target - numbers[i]

        if aim in seen:
            output.append(seen[aim])
            output.append(i)
            return output
        seen[numbers[i]] = i
        
    
def max_profit(prices):

    profit = 0
    buy = prices[0]

    for price in prices:
        if price < buy:
            buy = price

        if price - buy > profit:
            profit = price - buy
    return(profit)
# 

def valud_parentehses(sentance):

    closed = {
        ")": "(",
        "}": "{",
        "]": "["
    }

    stack = []
    string = list(sentace)

    for i in range(len(sentance)):
        if string[i] in closed:
            if not stack or stack[-1] !=  closed[string[i]]:
                return False
            stack.pop()

        else:
            stack.append(string[i])

    return not stack






def checks(sentance):

    stack = []
    string = list(sentance)
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    for i in range(len(sentance)):
        if string[i] in pairs:
            if not stack or stack[-1] != pairs[string[i]]:
                return False
            stack.pop()

        else:
            stack.append(string[i])

    return not stack




def closing(sentance):

    closed = {
        ")": "(",
        "]": "[",
        "}": "{"
        }

    stack = []
    word = list(sentance)

    for i in range(len(word)):
        if word[i] in closed:
            if not stack or stack[-1] != closed[word[i]]:
                return False
            stack.pop()
        else:
            stack.append(word[i])
        
    return not stack


def move_zeros(numbers):
    output = []
    count_zeros = 0
    for i in range(len(numbers)):
        if numbers[i] == 0:
            count_zeros += 1
        else:
            output.append(numbers[i])
    
    output.extend([0] * count_zeros)
    return output
        

def most_common(numbers):
    seen = {}
    maximum_no = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] in seen:
            seen[numbers[i]] += 1
            if seen[numbers[i]] > seen[maximum_no]:
                maximum_no = numbers[i]
        else:
            seen[numbers[i]] = 1
    return maximum_no




