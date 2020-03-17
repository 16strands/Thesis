##################
## Node classes ##
##################


## Imports ##

from random import randint
from EIGNode import EIGNode, EIGTree
from event import ReceiveEvent, TimeoutEvent, DecisionEvent


## Constants ##

LATENCY_MAX = 20
TIMEOUT = 200 # TODO figure out good timeout number


## Process Superclass ##

class Process:
    def __init__(self, name, gsr):
        self.name = name
        self.round = 1
        self.drift = randint(0, 50)
        self.gsr = gsr


    # def __repr__(self):
    #     rep = "(Name: " + str(self.name) + ", InitVal: " + str(self.initialValue) + ") "
    #     return rep

    # Alternative string repr
    #
    # def __repr__(self):
    #     return str(self.name)

    def __repr__(self):
        return str(self.name) + ", " + str(self.round) + ", " + str(self.drift)

    def updateDrift(self):
        if self.drift > 0:
            self.drift -= randint(0, 20)
        if self.drift < 0:
            self.drift = 0

    def isHonest(self):
        raise NotImplementedError("isHonest must be implemented by subclasses")

    def sendToAll(self, network):
        # If this is the final round, add a decision event to the queue
        if (self.round == network.getMaxByz() - 1): # TODO: check this
            print("final round: " + str(self))
            decision = self.decide(self.getEIGRoot(), network)
            decisionEvent = DecisionEvent(self, decision, network)
            delay = self.drift + randint(0, LATENCY_MAX)
            network.addToQueue(decisionEvent, delay)
        # Otherwise broadcast and then add timeout event to queue
        else:
            for node in self.tree.getLevel(network.getRoundNum() - 1):
                if self not in node.getParents():
                    if node.val != None:
                        self.broadcast(node, network)
            timeoutEvent = TimeoutEvent(self, network)
            network.addToQueue(timeoutEvent, TIMEOUT + self.drift)

    def broadcast(self, node, network):
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

    def receive(self, sender, node, network):
        if self.round == node.round:
            newParents = node.parents[:]
            newParents.append(sender)
            newVal = node.val
            newNode = EIGNode(newVal, newParents, (self.round + 1))
            self.tree.getNodeFromParents(node.parents).updateChildren(newNode)
            self.currentLevel.append(newNode)
            self.receivedFromThisRound.append(sender)
        else:
            network.log.debug(str(self) + " missed input in round " + str(self.round - 1) + " from " + str(sender))
            network.log.debug(str(node))

    def updateTree(self):
        self.tree.addLevel(self.currentLevel)
        self.currentLevel = []
        self.receivedFromThisRound = []

    def getEIGRoot(self):
        return self.tree.getRoot()

    def printEIGLevels(self):
        return self.tree.printVals()

    def timeout(self, network):
        network.log.debug(str(self) + "ended round: " + str(self.round))
        self.round += 1
        self.updateTree()
        self.updateDrift()  # TODO: drift only updates at the end of each round
        self.sendToAll(network)



## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, gsr, val):
        Process.__init__(self, name, gsr)
        self.initialValue = val
        self.tree = EIGTree(EIGNode(self.initialValue, ["root"], 0))
        self.currentLevel = []
        self.lastTimeoutQueued = None
        self.receivedFromThisRound = []

    def isHonest(self):
        return True

    # Enqueues one event for every other process
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                delay = self.drift + randint(0, LATENCY_MAX)
                network.addToQueue(event, delay)


## Byzantine Node ##

class ByzantineProcess(Process):

    def __init__(self, name, gsr, range):
        Process.__init__(self, name, gsr)
        self.range = range
        self.initialValue = self.getRandomValFromRange()
        self.tree = EIGTree(EIGNode(self.initialValue, ["root"], 0))
        self.lastTimeoutQueued = None
        self.receivedFromThisRound = []
        self.currentLevel = []

    def isHonest(self):
        return False

    def getRandomValFromRange(self):
        return randint(self.range[0], self.range[0])

    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                newVal = self.getRandomValFromRange()
                newNode = EIGNode(newVal, node.getParents(), (self.round + 1))
                event = ReceiveEvent(self, receiver, newNode, network)
                delay = self.drift + randint(0, LATENCY_MAX)
                network.addToQueue(event, delay)


## Crashed Process ##

class CrashedProcess(Process): # TODO: make crashed processes be able to crash after a certain time

    def __init__(self, name, crashTime):
        Process.__init__(self, name)
        self.crashTime = crashTime

    def decide(self):
        pass

    def broadcast(self, eventQueue, t):
        pass

