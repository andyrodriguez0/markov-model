
from collections.abc import MutableMapping

class Hashtable(MutableMapping):

    # Polynomial constant used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        '''
        This method specifies the actions to be taken when a new Hastable is
        created

        Inputs:
            - capacity (int): an integer representing the initial capacity of
            the Hashtable
            - default_value: a value representing the value to be returned when
            searching for a key not in the Hashtable
            - load_factor (float): a float representing the maximum occupancy
            of the Hashtable before it is resized
            - growth_factor (int): an integer representing the amount by which
            the Hashtable will grow while resizing
        
        Outputs:
            - None
        '''

        # Initialize the input attributes
        self.capacity = capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor

        # Initialize additional attributes
        self._items = [self.default_value for _ in range(self.capacity)]
        self.count = 0

    def _hash(self, key):
        '''
        This method takes in a string and returns an integer value between 0
        and self.capacity. This particular hash function uses Horner's rule to
        compute a large polynomial. See
        https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf

        Inputs:
            - key (str): a string representing the key that will be hashed
        
        Outputs:
            - (int): an integer representing the hash value of the key
        '''

        # Initialize variables
        val = 0

        # Calculate the hash value
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)

        return val % self.capacity

    def __setitem__(self, key, val):
        '''
        This method implements the __setitem__ behavior for a Hashtable

        Inputs:
            - key (str): a string representing the key in the Hashtable
            - value: a value representing the value associated with the key
        
        Outputs:
            - None
        '''
        
        # Initialize variables
        index = self._hash(key)
        current = self._items[index]
        deleted = None

        # Iterate through the Hashtable until you find an empty cell or the key
        while current != self.default_value and current[0] != key:

            # If you find a deleted cell, mark it
            if not current[2] and not deleted:
                deleted = index
            
            # Move on to the next entry
            index = (index + 1) % self.capacity
            current = self._items[index]
        
        # If you found an empty cell, increase the count by one
        # If you found a deleted entry, use that one instead
        if current == self.default_value:
            self.count += 1
            if deleted:
                index = deleted
        
        # If you found the key, increase the count by one if it was deleted
        else:
            if not current[2]:
                self.count += 1

        # Set the item
        self._items[index] = (key, val, True)

        # If the load factor is reached, rehash the Hashtable
        if len(self) / self.capacity >= self.load_factor:
            self._rehash()

    def __getitem__(self, key):
        '''
        This method implements the __getitem__ behavior for a Hashtable

        Inputs:
            - key (str): a string representing the key to be searched
        
        Outputs:
            - the value associated with the key if the key is in the Hashtable
            or the default value otherwise
        '''
        
        # Initialize variables
        index = self._hash(key)
        current = self._items[index]

        # Iterate through the Hashtable until you find an empty cell or the key
        while current != self.default_value and current[0] != key:

            # Move on to the next entry
            index = (index + 1) % self.capacity
            current = self._items[index]

        # If you found an empty cell or the key has been deleted, return the
        # default value
        if current == self.default_value or not current[2]:
            return self.default_value

        return current[1]

    def __delitem__(self, key):
        '''
        This method implements the __delitem__ behavior for a Hashtable

        Inputs:
            - key (str): a string representing the key to be deleted
        
        Outputs:
            - None
        '''
        
        # Initialize variables
        index = self._hash(key)
        current = self._items[index]

        # Iterate through the Hashtable until you find an empty cell or the key
        while current != self.default_value and current[0] != key:

            # Move on to the next entry
            index = (index + 1) % self.capacity
            current = self._items[index]

        # If you found the key, delete the entry and update the count
        if current != self.default_value and current[2]:
            self._items[index] = (current[0], current[1], False)
            self.count -= 1
        
        # Raise a KeyError if the key was not in the Hashtable
        else:
            raise KeyError

    def __len__(self):
        '''
        This method implements the __len__ behavior for a Hashtable

        Inputs:
            - None
        
        Outputs:
            - self.count (int): the number of items in the Hashtable
        '''
        
        return self.count
    
    def _rehash(self):
        '''
        This method rehashes the Hashtable after the load factor has been
        reached

        Inputs:
            - None
        
        Outputs:
            - None
        '''

        # Store the current items
        items = self._items

        # Increase the capacity and reset the items and the count
        self.capacity *= self.growth_factor
        self._items = [self.default_value for _ in range(self.capacity)]
        self.count = 0

        # Rehash all of the items in the Hashtable
        for item in items:
            if item != self.default_value and item[2]:
                self[item[0]] = item[1]

    def __iter__(self):
        '''
        You do not need to implement __iter__ for this assignment. This stub is
        needed to satisfy `MutableMapping` however. Note, by not implementing
        __iter__ your implementation of Markov will not be able to use things
        that depend upon it. That shouldn't be a problem but you'll want to
        keep that in mind.

        Inputs:
            - None
        
        Outputs:
            - None
        '''

        raise NotImplementedError("__iter__ not implemented")