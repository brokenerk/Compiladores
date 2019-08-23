class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    def push(self, item):
        self.items.insert(0, item)
    
    def pop(self):
        return self.items.pop(0)
    
    def top(self):
        idx = len(self) -1
        return print(self.items[idx])
    
    def printStack(self):
        return print(self.items)