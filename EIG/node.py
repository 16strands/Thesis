##################
## Node classes ##
##################


## Imports ##

from random import randint


## Constants ##

TIMEOUT = 200 # TODO figure out good timeout number


## Node Superclass ##

class Node:
    def __init__(self, name):
        self.name = name
        self.round = 0

    def __repr__(self):
        raise NotImplementedError("Repr must be implemented by subclasses")

    def decide(self):
        raise NotImplementedError("Decision function must be implemented by subclasses")

    def broadcast(self, eventQueue, t):  # TODO: t here?
        raise NotImplementedError("Broadcast method must be implemented by subclasses")
        #call some global function with sender, receiver and time as input, and latency
        # system call to send messages 

    def receive(self, eventQueue): # event triggers at time specified at broadcast time
        raise NotImplementedError("Receive method must be implemented by subclasses")


## Honest Node ##

class HonestNode(Node):

    def __init__(self, name, val):
        Node.__init__(self, name)
        self.initialValue = val
        self.tree = {("root", self.initialValue)} # TODO: Figure out how to structure this better

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: " + str(self.initialValue) + ")"
        return rep

    def decide(self):
        pass # TODO: figure out decision function based on structure of EIG tree

    def broadcast(self, eventQueue, t):
        # lower level send and recieve methods than broadcast
        # Broadcast "makes this thing happen"
        # recieve method stores bit that stores whether we're in broadcast
        eventQueue.enqueue(("current string of vals alpha"), 200) # TODO: this is not right at all
        eventQueue.enqueue(("TIMEOUT"), 200+TIMEOUT)

    def receive(self, eventQueue):
        # If curently in broadcast do this , otherwise do that
        # or separate broadcast recieve funtion
        pass # TODO


## Byzantine Node ##

class ByzantineNode(Node):

    def __init__(self, name, range):
        Node.__init__(self, name)
        self.range = range
        self.initialValue = randint(range[0], range[1])
        self.tree = {("root", self.initialValue)} # TODO: can this move to superclass?

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: " + str(self.initialValue) + ")"
        return rep

    def decide(self):
        pass # TODO: return random val? what does it mean to decide if you're byzantine? fully random?

    def broadcast(self, eventQueue, t):
        pass # TODO: figure this one out

    def receive(self, eventQueue, t):
        pass # TODO


## Crashed Node ##

class CrashedNode(Node): # TODO: make crashed nodes be able to crash after a certain time

    def __init__(self, name, crashTime):
        Node.__init__(self, name)
        self.crashTime = crashTime

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: CRASHED)"
        return rep

    def decide(self):
        pass

    def broadcast(self, eventQueue, t):
        pass


## EIG Node ##

# TODO: Move this to separate file

class EIGNode():  # TODO: what does an EIG tree look like
    def __init__(self, level, val, children):
        self.level = level
        self.val = val
        self.children = children


# STring and a val!! like n1n2n3, 4

