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
