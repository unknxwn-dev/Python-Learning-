
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

