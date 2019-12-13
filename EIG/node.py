################
# Node classes #
################

from random import randint

TIMEOUT = 200 # TODO figure out good timeout number

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
        eventQueue.enqueue(("current string of vals alpha"), 200) # TODO: this is not right at all
        eventQueue.enqueue(("TIMEOUT"), 200+TIMEOUT)

    def receive(self, eventQueue):
        pass # TODO


class ByzantineNode(Node):

    def __init__(self, name, range):
        Node.__init__(self, name)
        self.range = range
        self.initialValue = randint(range[0], range[1])
        self.tree = {("root", self.initialValue)} # TODO: Figure out how to structure this better

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: " + str(self.initialValue) + ")"
        return rep

    def decide(self):
        pass # TODO: return random val? what does it mean to decide if you're byzantine? fully random?

    def broadcast(self, eventQueue, t):
        pass # TODO: figure this one out

    def receive(self, eventQueue, t):
        pass # TODO


class CrashedNode(Node): # TODO: make crashed nodes be able to crash after a certain time

    def __init__(self, name):
        Node.__init__(self, name)

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: CRASHED)"
        return rep

    def decide(self):
        pass

    def broadcast(self, eventQueue, t):
        pass
        

class EIGNode():  # what does an EIG tree even look like bruh...
    def __init__(self, level, val, children):
        self.level = level
        self.val = val
        self.children = children


