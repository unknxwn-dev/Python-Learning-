#Algorithms have two key characteristics:

#They cannot continue indefinitely. They must finish in a finite number of steps.
#Each step must be precise and unambiguous.



# the Big O 
#  Quadratice time complexity == O(N^2)
# Constant time complexity == O(1)
# Logarithmic Time Complexity == O(log n)
# Linear Time Complexity == O(n)
# Log-Linear Time Complexity == O(n log n)  
#       This is common fro sorting 
# Exponential Time Complexity == O(2^n)
# Factorial Time Complexity == O(n!)
# 
# In this context it describes how the memory space grows 
# 
# 
# Pseudocode helps write in english whats goung on 
# 
#       GET original_string

#       SET reversed_string = ""

#       FOR EACH character IN original_string:
  #          ADD character TO THE BEGINNING OF reversed_string

#       DISPLAY reversed_string

# there will be many ways, you must find the most efficient 
# way to do thisd 

#
# "How will I approach this problem?"
"What data structures will I use?"
"Are the data structures that I chose the most efficient ones for the problem at hand?"
"Am I covering all possible edge cases?"
# 


# 
# Dynamic Arrays and Static Arrays 
# 
# Arrays are a data structure, they store ordered data
# 
# Static arrays have a fixed size, they store elements in adjacent memory location 
#       Size is determined when initialized
#       Adjacent memory makes the process more efficient
#           This means accessing elements is O(1)
# 
#  
# Dynamic Arrays are more flexible, they can grow or shrink automatically
#       Accessing elements is O(1)
#       Inserting elements is O(n) --> Middle 
#                          is O(1) --> End if there is space 
#                          is O(n) --> If needs resizing
# List [] is a type of dynamic array 
# 

# 
# Stacks adn Queues are data structures 
# 

# Stacks 
# LIFO structure 
# Adding an element is a PUSH operation 
# Removing is a POP operation 
#       The time complexity is O(1)
# 

# QUEUES  
# FIFO structure 
#   THey have two ends, front and back
#   Elements are added to the back and removed from the front 
# 
# Adding is known as ENQUEUE 
# Removing is known as DEQUEUE
# 
# Both are O(1)
# 

# 
# Singly Linekd Lists & Doubly Linked List
# 

# A linked List is a linear data structure, where each node is connected to the next node in sequence  
#   This creats a chain of nodes
# 
# Linked list are used for implementing other data structure
# 

# Singly Linked Lists 
#   type of linked lists whcih each node is connected to the next node in sequence
#   linked through a reference --> Allowing you to traverse the linekd list in one direction  
#       It can only move forward not backwards
# 
# The head node is usually the only onode that is directly accessible START 
#       This is the search process will start when youre trying to find a specific node 
# The tail node is the last node
# 

# Inserting Nodes 
#  They do not have a fixed size 
#   You can add a node at the start, middle or end of a linked list 
# 
#   Linekd lists dont need a specific order, but you can implement it in your code and the criteria 
#  
# Linking at start = O(1) | At end O(n)
# 
# 

# Removing nodes 
# O(1) as it only requires updating the reference 
# 
#  You would need to form a bridge if removing from the middle
# 
# End list is O(n)
# 

# Doubly Linekd Lists
#   It holds references to the next node and the previous node
#       Allowing travers in both directions 
#       you should keep track of Tail node to start traversal from the end  
#  They take up more memory than single
# 
# You will have to update two references per node 
#  and keep track of the reference to the tail 
# 

# 
# Maps, Hash Maps and Sets   
# 
# Abstract Data Type (ADT)
#   a conceptual representation fo a data type 
#   It includes what operations can be performed and the properties
# They are like blueprints that describe WHAT operations can be performed, not HOW they are
# 

#  MAP is an ADT that maaes collections of key-value pairs and thier operations  
#  Characteristics include 
#         - Key must be unique --> ALlow direct lookups 
#           
# 
#   If there are two keys reult in the saem index
#   Hash maps solve this but CHAINING where each array index points to a linked list
#   This will stroe all the elements witht eh same index
# 
#   Another way is OPEN ADDRESSING --> involves searching for the next availble index in the array based ona  predefined search sequece 
# 
#   Hash maps O(1) for inserting retrieveing and deleting 
#       if there is a lot of collisions itll be O(n)
# del my_dictionary['hey']
# in function and reassising 

# 
# SETS, unordered collections of unique elemebts 
#   - You cannot acces them through indices
#   - Only contain unique elements
# 
# They are analogous to sets in mathematics, they have operations
#   - Intersection
#   - Union
#   - Difference
# 
# Inserting, removing, len() --> O(1)
# 
# .remove() --> will cause a KeyError if not found use .discard()
# .add
# .pop()  --> returns an arbitrary elelemt
# .clear()
# in function
#
# 
set_a = {1, 2, 3, 4}
set_b = {2, 3, 4, 5, 6}

set_a.union(set_b)
set_a.intersection(set_b)
set_a.symmetric_difference(set_b)
set_a.difference(set_b)
# equivalent operators:
set_a | set_b
set_a & set_b
set_a ^ set_b
set_a - set_b 
# This is all O(1)
# 
set_a.issubset(set_b)   # This checks if there is a in b 
set_a.issuperset(set_b) # This checks if there is b in a 

# 
# 
# 
# 

class LinkedList:
    class Node:
        def __init__(self, element):
            self.element = element
            self.next = None    #  Sets the direction to nothing 
            
    def __init__(self):
        self.length = 0         # initalises the lenght to 0 
        self.head = None        #  Shows there is no Head Node

    def is_empty(self):
        return self.length == 0 # Returns true if == 0 ansd False if >0

    def add(self, element):
        node = self.Node(element)       # this assings the instance of Node, adding a new node to the linked list 
        if self.is_empty():             # Checks if it is empty
            self.head = node            # Assigns first node to head node 
        else:
            current_node = self.head    #  passes makes the current the head
            while current_node.next is not None:    #  checks it is not at end
                current_node = current_node.next    #  continues down the line 
            current_node.next = node                #  Makes the node = the next 
        self.length += 1    # Increases the length by 1 

    def remove(self, element):
        previous_node = None    # sets the previous nodes 
        current_node  = self.head        # sets the head 
        while current_node is not None and current_node.element != element: # This checks its not at the end or at the element we want to remove 
            previous_node = current_node        # this traverse setting the previous node
            current_node = current_node.next    # and the next node as our making it go forward
        if current_node is None:    # If this occurs, we havent found th erequried element 
            return  #Breaks the loop 
        elif previous_node is not None: # this checks if the element to be remove is found is not the head node
            previous_node.next = current_node.next  # this will update to skip over the current node ( to be removed)
        else:
            self.head = current_node.next   # this makes sure the element isnt the head and if so, makes it so we can remove it 
        self.length -= 1    # decreases the length 
my_list = LinkedList()          # Calls the instance
print(my_list.is_empty())       # Checks if it is empty

my_list.add(1)
my_list.add(2)
print(my_list.is_empty())
print(my_list.length)

my_list.remove(1)
print(my_list.length)




#  #
class HashTable:
    def __init__(self):
        self.collection = {

        }
    
    def hash(self, string: str):
        hash_output = 0
        for i in string:
            hash_output += ord(i)
        return hash_output

    def add(self, key, value):
        
        key_output = 0
        for i in key: 
            key_output += ord(i)
        if key_output in self.collection.keys():
            self.collection[key_output][key] = value
        else:
            self.collection[key_output] = {
            key: value
            }

    def remove(self, key):
        key_output = 0
        for i in key: 
            key_output += ord(i)
        if key_output in self.collection.keys() and key in self.collection[key_output]:
            del self.collection[key_output][key]
        

    def lookup(self, key):
        key_output = 0
        for i in key: 
            key_output += ord(i)

        if key_output not in self.collection or key not in self.collection[key_output]:
            return None
        else:
            return self.collection[key_output][key]

HashTable().hash('golf')
