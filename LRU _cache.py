class ListNode:
    def __init__(self, value, key):
        self.value = value
        self.next = None
        self.prev = None
        self.key = key
        
class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.head = None
        self.tail = None
        self.dict_storage = {}
    
    def remove_tail(self):
        ##removes tail
        if self.tail:
            new_tail = self.tail.prev ##tail.prev may be None
        ##tail.before becomes new tail
            if new_tail:
                new_tail.next = None
            self.tail = new_tail
        ##DOESN'T CHANGE SIZE OR UPDATES DICT
    
    def new_head(self, new_head):
        ##checks if new_head is already the head
        if self.head:
            if new_head != self.head:
        ##if not, new_head becomes head and leads to the old head
                new_head.next = self.head
                self.head.prev = new_head
        else:
            new_head.next = None
            self.tail = new_head
        new_head.prev = None
        self.head = new_head
        ##DOESN´T CHANGE SIZE OR UPDATES DICT
        
    def update(self, key):
        """
        recives a key in dict_storage and makes it the new head and updates the other nodes accordingly
        """
        before = self.dict_storage[key].prev ##may be None
        after = self.dict_storage[key].next ##may be None
        if before and after: ##key is neither head nor tail
            before.next = after
            after.prev = before
            self.new_head(self.dict_storage[key])
        elif not before: ##key is already head
            pass
        elif not after: ##key is the tail, but not the head
            self.remove_tail()
            self.new_head(self.dict_storage[key])   
            
    def get(self, key):
        ##if key is not in dict, returns -1
        if key not in self.dict_storage:
            return -1
        self.update(key)
        return self.dict_storage[key].value
    
    def put(self, key, value):
        ##if key is in dict
        if key in self.dict_storage:
        ##updates value
            self.dict_storage[key].value = value
        ##key is now the new head
            self.update(key)
        ##if key is not in dict
        else:
        ##key is the new head
            node = ListNode(value, key)
            self.new_head(node)
        ##size increases by one
            self.size += 1
        ##dict is updated
            self.dict_storage[key] = node
        ##if size is now bigger than capacity
            if self.size > self.capacity:
        ##updates dict
                self.dict_storage.pop(self.tail.key)
        ##removes tail
                self.remove_tail()
        ##decreases size by one
                self.size -= 1