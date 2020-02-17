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
        rep = "(Name: " + str(self.name) + ", InitVal: " + str(self.initialValue) + ") "
        return rep
    #
    # def __repr__(self):
    #     return str(self.name)

    def isHonest(self):
        raise NotImplementedError("isHonest must be implemented by subclasses")


    def decide(self, node):
        raise NotImplementedError("Decision function must be implemented by subclasses")

    def sendToAll(self, network, latency):
        # lower level send and receive methods than broadcast
        # Broadcast "makes this thing happen"
        # receive method stores bit that stores whether we're in broadcast
        for node in self.tree.getLevel(network.getRoundNum() - 1):
            if self not in node.getParents():
                if node.val != None:
                    self.broadcast(node, network, latency)
        # self.lastTimeoutQueued = TimeoutEvent(self, network)
        # return self.lastTimeoutQueued

    def broadcast(self, node, network, latency):  # TODO: t here?
        raise NotImplementedError("Broadcast method must be implemented by subclasses")
        #call some global function with sender, receiver and time as input, and latency
        # system call to send messages

    def decide(self, node, network):
        if node.getChildren() == False:
            return node.val
        else:
            vals = []
            repeated = {}
            for child in node.getChildren():
                vals.append(self.decide(child, network))
            for val in vals:
                if val in repeated:
                    repeated[val] += 1
                else:
                    repeated[val] = 1
            for val in repeated.keys():
                if repeated[val] >= len(network.getProcesses()) - len(node.getParents()) - network.getMaxByz():
                    return val

    def receive(self, sender, node, network):
        # If currently in broadcast do this , otherwise do that
        # or separate broadcast receive function
        assert(len(self.tree.tree) == network.getRoundNum())
        newParents = node.parents[:]
        newParents.append(sender)
        newVal = node.val
        newNode = EIGNode(newVal, newParents)
        self.tree.getNodeFromParents(node.parents).updateChildren(newNode)
        self.currentLevel.append(newNode)
        self.receivedFromThisRound.append(sender)
        # if len(self.currentLevel) >= len(network.getProcesses()):
        #     network.log.debug(str(self) + "Removing timeout for " + str(self))
        #     network.removeFromQueue(self.lastTimeoutQueued)

    def updateTree(self):
        self.tree.addLevel(self.currentLevel)
        self.currentLevel = []
        self.receivedFromThisRound = []

    def getEIGRoot(self):
        return self.tree.getRoot()

    def printEIGLevels(self):
        return self.tree.printVals()

## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, val):
        Process.__init__(self, name)
        self.initialValue = val
        self.tree = EIGTree(EIGNode(self.initialValue, ["root"]))
        self.currentLevel = []
        self.lastTimeoutQueued = None
        self.receivedFromThisRound = []

    def isHonest(self):
        return True

    # Enqueues one event for every other process
    def broadcast(self, node, network, latency):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                network.addToQueue(event, latency)

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
        self.tree = EIGTree(EIGNode(self.initialValue, ["root"]))
        self.lastTimeoutQueued = None
        self.receivedFromThisRound = []
        self.currentLevel = []

    def isHonest(self):
        return False

    def broadcast(self, node, network, latency):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                network.addToQueue(event, latency)


## Crashed Process ##

class CrashedProcess(Process): # TODO: make crashed processes be able to crash after a certain time

    def __init__(self, name, crashTime):
        Process.__init__(self, name)
        self.crashTime = crashTime

    def decide(self):
        pass

    def broadcast(self, eventQueue, t):
        pass

