##################
## Node classes ##
##################


## Imports ##

from random import randint
from EIGNode import EIGNode, EIGTree
from event import ReceiveEvent, TimeoutEvent


## Constants ##

TIMEOUT = 200 # TODO figure out good timeout number
NOISE_RANGE = (1, 200)  # Gaussian sample from range ?


## Process Superclass ##

class Process:
    def __init__(self, name):
        self.name = name
        self.round = 0

    def __repr__(self):
        raise NotImplementedError("Repr must be implemented by subclasses")

    def decide(self):
        raise NotImplementedError("Decision function must be implemented by subclasses")

    def sendToAll(self, eventQueue, t, r):
        raise NotImplementedError("sendToAll function must be implemented by subclasses")

    def broadcast(self, eventQueue, t):  # TODO: t here?
        raise NotImplementedError("Broadcast method must be implemented by subclasses")
        #call some global function with sender, receiver and time as input, and latency
        # system call to send messages 

    def receive(self, eventQueue): # event triggers at time specified at broadcast time
        raise NotImplementedError("Receive method must be implemented by subclasses")


## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, val):
        Process.__init__(self, name)
        self.initialValue = val
        self.tree = EIGTree(EIGNode(self.initialValue, ["root"]))
        self.currentLevel = []
        self.lastTimeoutQueued = None
        self.receivedFromThisRound = []

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: " + str(self.initialValue) + ")"
        return rep

    def decide(self):
        pass # TODO: figure out decision function based on structure of EIG tree

    def sendToAll(self, network, latency):
        # lower level send and receive methods than broadcast
        # Broadcast "makes this thing happen"
        # receive method stores bit that stores whether we're in broadcast
        for node in self.tree.getLevel(network.getRoundNum() - 1):
            print("!!!!!!!!")
            print(self.name)
            print(node.parents)
            print(str(self.name in node.parents))
            if self.name not in node.parents:
                if node.val != None:
                    self.broadcast(node, network, latency)
        # self.lastTimeoutQueued = TimeoutEvent(self, network)
        # return self.lastTimeoutQueued

    # Enqueues one event for every other process
    def broadcast(self, node, network, latency):
        for receiver in network.getProcesses():
            event = ReceiveEvent(self, receiver, node, network)
            network.addToQueue(event, latency)



    def receive(self, sender, node, network):
        # If currently in broadcast do this , otherwise do that
        # or separate broadcast receive function
        assert(len(self.tree.tree) == network.getRoundNum())
        newParents = node.parents[:]
        newParents.append(sender)
        newVal = node.val
        newNode = EIGNode(newVal, newParents)
        self.currentLevel.append(newNode)
        self.receivedFromThisRound.append(sender)
        print(len(self.currentLevel))
        print(len(network.getProcesses()))
        # if len(self.currentLevel) >= len(network.getProcesses()):
        #     network.log.debug(str(self) + "Removing timeout for " + str(self))
        #     network.removeFromQueue(self.lastTimeoutQueued)

    def updateTree(self):
        self.tree.addLevel(self.currentLevel)
        self.currentLevel = []
        self.receivedFromThisRound = []

    # def timeout(self, network):  # no, processes are recieving multiple messages from each other processor during each round
    #     timedOut = []
    #     for process in network.getProcesses():
    #         if process not in self.receivedFromThisRound:
    #             timedOut.append(process)
    #     for process in timedOut:
    #         newNode = newNode = EIGNode(None, node.parents.append(sender))
    #     self.currentLevel.append(newNode)



## Byzantine Node ##

class ByzantineProcess(Process):

    def __init__(self, name, range):
        Process.__init__(self, name)
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


## Crashed Process ##

class CrashedProcess(Process): # TODO: make crashed processes be able to crash after a certain time

    def __init__(self, name, crashTime):
        Process.__init__(self, name)
        self.crashTime = crashTime

    def __repr__(self):
        rep = "(Name: " + self.name + ", InitVal: CRASHED)"
        return rep

    def decide(self):
        pass

    def broadcast(self, eventQueue, t):
        pass

