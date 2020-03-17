#####################
## Process classes ##
#####################


## Imports ##

from random import randint
from eigTree import EIGNode, EIGTree
from event import ReceiveEvent, TimeoutEvent, DecisionEvent


## Constants ##

LATENCY_MAX = 20
TIMEOUT = 200 # TODO figure out good timeout number
DRIFT = 50

## Process Superclass ##

class Process:
    def __init__(self, name, gsr):
        self.name = name
        self.round = 1
        self.drift = randint(0, DRIFT)
        self.gsr = gsr

    # uncomment desired repr method

    # prints name, init val
    # def __repr__(self):
    #     rep = "(Name: " + str(self.name) + ", InitVal: " + str(self.initialValue) + ") "
    #     return rep

    # only prints name
    #
    # def __repr__(self):
    #     return str(self.name)

    # prints name, round, and drift
    def __repr__(self):
        return str(self.name) + ", " + str(self.round) + ", " + str(self.drift)

    # TODO: make this better
    def updateDrift(self):
        if self.drift > 0:
            self.drift -= randint(0, 20)
        if self.drift < 0:
            self.drift = 0

    def isHonest(self):
        raise NotImplementedError("isHonest must be implemented by subclasses")

    # pick which nodes to broadcast, call broadcast for each, add timeout event to queue
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
            for node in self.tree.getLevel(self.round - 1):
                if self not in node.getParents():
                    if node.val != None:
                        self.broadcast(node, network)
            # add timeout event to queue
            timeoutEvent = TimeoutEvent(self, network)
            network.addToQueue(timeoutEvent, TIMEOUT + self.drift)

    def broadcast(self, node, network):
        raise NotImplementedError("Broadcast method must be implemented by subclasses")

    # decide on a final value based on EIG tree, see alg 1 for explanation
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

    # receive incoming node and add to current level of tree
    def receive(self, sender, node, network):
        # print("myRound: " + str(self.round) + ", nodeRound: " + str(node.round))
        if self.round == node.round:
            print("!!!!!!!!!")
            newParents = node.parents[:]
            newParents.append(sender)
            newVal = node.val
            newNode = EIGNode(newVal, newParents, (self.round))
            self.tree.getNodeFromParents(node.parents).updateChildren(newNode)
            self.currentLevel.append(newNode)
        else:
            print("????????")
            network.log.debug(str(self) + " missed input in round " + str(self.round) + " from " + str(sender))
            network.log.debug(str(node))

    # add current level to tree
    def updateTree(self):
        self.tree.addLevel(self.currentLevel)
        self.currentLevel = []

    def getEIGRoot(self):
        return self.tree.getRoot()

    def printEIGLevels(self):
        return self.tree.printVals()

    # increment round, update EIG tree, update drift, call sendToAll
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
        self.currentLevel = []  # for building levels of tree before updating main tree

    def isHonest(self):
        return True

    # Enqueues one receive event for every other process
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
        self.currentLevel = []  # for building levels of tree before updating main tree

    def isHonest(self):
        return False

    def getRandomValFromRange(self):
        return randint(self.range[0], self.range[0])

    # Enqueues one receive event for every other process, but with random vals from range
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                newVal = self.getRandomValFromRange()
                newNode = EIGNode(newVal, node.getParents(), (self.round))
                event = ReceiveEvent(self, receiver, newNode, network)
                delay = self.drift + randint(0, LATENCY_MAX)
                network.addToQueue(event, delay)
