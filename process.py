##################
## Node classes ##
##################


## Imports ##

from random import randint
from EIGNode import EIGNode, EIGTree
from event import ReceiveEvent, TimeoutEvent


## Constants ##

TIMEOUT = 200 # TODO figure out good timeout number


## Process Superclass ##

class Process:
    def __init__(self, name):
        self.receiving = True
        self.name = name
        self.round = 0
        self.baseLatency = 20 # TODO: write function to slightly randomize this

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

    def sendToAll(self, network):
        for node in self.tree.getLevel(network.getRoundNum() - 1):
            if self not in node.getParents():
                if node.val != None:
                    self.broadcast(node, network, latency)
        timeoutEvent = TimeoutEvent(self, network)
        network.addToQueue(timeoutEvent, TIMEOUT + self.baseLatency)

    def broadcast(self, node, network, latency):  # TODO: t here?
        raise NotImplementedError("Broadcast method must be implemented by subclasses")

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
                if repeated[val] >= len(network.getProcesses()) - len(node.getParents()) - network.getMaxByz(): # TODO: check for condition of correctness
                    return val
                else:
                    network.log.debug("No agreement on a value at this level.")

    def receive(self, sender, node, network):  # TODO: parameter not used
        if self.receiving == True:
            newParents = node.parents[:]
            newParents.append(sender)
            newVal = node.val
            newNode = EIGNode(newVal, newParents)
            self.tree.getNodeFromParents(node.parents).updateChildren(newNode)
            self.currentLevel.append(newNode)
            self.receivedFromThisRound.append(sender)

    def updateTree(self):
        self.tree.addLevel(self.currentLevel)
        self.currentLevel = []
        self.receivedFromThisRound = []
        self.receiving = True

    def getEIGRoot(self):
        return self.tree.getRoot()

    def printEIGLevels(self):
        return self.tree.printVals()

    def timeout(self):
        self.receive = False


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

