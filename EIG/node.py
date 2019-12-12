class Node():
    def __init__(self, byz, name, val):
        self.byz = byz
        self.name = name # is this necessary?
        self.initialValue = val
        self.round = 0
        self.tree = {("root", self.initialValue)} # Figure out how to structure this better

    def decide(self):
        pass

    def broadcast(self):  # return the value to be brodcasted
        pass
        #call some global function with sender, receiver and time as input, and latency
        # system call to send messages 

    def receive(self): # event triggers at time specified at broadcast time
        pass
        

class EIGNode():  # what does an EIG tree even look like bruh...
    def __init__(self, level, val, children):
        self.level = level
        self.val = val
        self.children = []


# make log file for debugging 

