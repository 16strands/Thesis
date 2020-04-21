#####################
## Process classes ##
#####################


## Imports ##

from eigNode import EIGNode
from event import ReceiveEvent, TimeoutEvent, DecisionEvent
from termcolor import colored
from treelib import Tree
import copy
from numpy import random

## Constants ##
TIMEOUT = 200.0 # TODO figure out good timeout number
DRIFT = 0

## Utility Functions ##
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele.name
    return str1

def getSmallestMostFrequentVal(vals, threshold=0, allowNone=True):
    repeated = {}
    if allowNone:
        for val in vals:
            if val in repeated:
                repeated[val] += 1
            else:
                repeated[val] = 1
    else:
        for val in vals:
            if val != None:
                if val in repeated:
                    repeated[val] += 1
                else:
                    repeated[val] = 1
    mostFrequent = (None, 0)
    for val in repeated.keys():
        if repeated[val] > mostFrequent[1]:
            mostFrequent = (val, repeated[val])
    if (mostFrequent[1] >= threshold):
        return mostFrequent[0]
    else:
        return None

## Process Superclass ##

class Process:
    def __init__(self, name, gsr):
        self.name = name
        self.round = 0
        self.drift = random.uniform(0, DRIFT)
        self.gsr = gsr
        self.decisionVector = []

    # uncomment desired repr method

    # prints name, init val
    # def __repr__(self):
    #     rep = "(Name: " + str(self.name) + ", InitVal: " + str(self.initialValue) + ") "
    #     return rep

    # only prints name

    def __repr__(self):
        return str(self.name)

    # prints name, round, and drift
    # def __repr__(self):
    #     return str(self.name) + ", " + str(self.round) + ", " + str(self.drift)

    # TODO: make this better, make it work with alg2 & gsr, as in the GSR needs to be _global_ and not within each EIG run
    def updateDrift(self):
        if self.drift > 0:
            self.drift -= random.uniform(0, 20)
        if self.drift < 0:
            self.drift = 0
        else:
            self.drift = 0

    def isHonest(self):
        raise NotImplementedError("isHonest must be implemented by subclasses")

    def isPrinter(self):
        raise NotImplementedError("isPrinter must be implemented by subclasses")

    # pick which nodes to broadcast, call broadcast for each, add timeout event to queue
    def sendToAll(self, network):
        # If this is the final round, add a decision event to the queue
        if (self.round == network.getMaxByz() + 1):
            if self.isPrinter():
                print(colored("adding decision event to queue in round " + str(self.round), 'blue'))
            self.decide(network)
            decisionEvent = DecisionEvent(self, self.decisionVector, network)
            latency = (random.lognormal(0.8, 0.5))*10  # See README for latency explanation
            delay = self.drift + latency
            network.addToQueue(decisionEvent, delay)
        # Otherwise broadcast and then add timeout event to queue
        else:
            if self.isPrinter():
                print(colored("sending to all round " + str(self.round), 'blue'))
            for node in self.tree.leaves():
                if self.round == 0:
                    if node.data.val != None:
                        if self.isPrinter():
                            print(colored("it is round 0, broadcasting " + str(node), 'green'))
                        newParents = node.data.parents[:]
                        newVal = node.data.val
                        newNode = EIGNode(newVal, newParents, self.round)
                        self.broadcast(newNode, network)
                if (self not in node.data.getParents()):
                    if self.isPrinter():
                        print(colored("i am not in parents of " + str(node), 'green'))
                    if node.data.val != None:
                        if self.isPrinter():
                            print(colored("val is not none, broadcasting " + str(node), 'green'))
                        newParents = node.data.parents[:]
                        newParents.append(self)
                        newVal = node.data.val
                        newNode = EIGNode(newVal, newParents, self.round)
                        self.broadcast(newNode, network)
                    elif node.data.val == None:
                        if self.isPrinter():
                            print(colored("value is none " + str(node), 'red'))
                elif self.round != 0:
                    if self.isPrinter():
                        print(colored("i am in parents of " + str(node), 'red'))

            # add timeout event to queue
            timeoutEvent = TimeoutEvent(self, network)
            network.addToQueue(timeoutEvent, TIMEOUT + self.drift)
            if self.isPrinter():
                print(colored("added timeout to queue round " + str(self.round), 'blue'))
                print(colored("timeout event: " + str(timeoutEvent), 'green'))

    def broadcast(self, node, network):
        raise NotImplementedError("Broadcast method must be implemented by subclasses")

        # decide on a final value based on EIG tree, see alg 1 for explanation
    def decideHelper(self, node, network):
        if len(self.tree.children(node.data.getParentsString())) == 0:
            return node.data.val
        else:
            vals = []
            for child in self.tree.children(node.data.getParentsString()):
                vals.append(self.decideHelper(child, network))
                val = getSmallestMostFrequentVal(vals, threshold=len(network.getProcesses()) - len(child.data.getParents()) - network.getMaxByz())
                if val != None:
                    return val
                else:
                    network.log.debug("No agreement on a value at this level.")
                    if self.isPrinter():
                        print(colored("no agreement on value at this level of tree", 'red'))

    def decide(self, network):
        if self.isPrinter():
            print(colored("deciding " + str(self.round), 'blue'))
            print("length of row 1: " + str(len(self.getEIGRoot().getChildren())))
        numOtherProcesses = len(network.getProcesses()) - 1
        decisionVector = []
        for child in self.tree.children("root"):
            decision = self.decideHelper(child, network)
            decisionVector.append((child.identifier, decision))
        # assert(len(decisionVector) == numOtherProcesses)
        decisionVector.append((self.name, self.initialValue))
        decisionVector.sort()
        self.decisionVector = decisionVector

    # receive incoming node and add to current level of tree
    def receive(self, sender, node, network):
        if self.isPrinter():
            print(colored("receiving event from " + str(sender) + " in round " + str(self.round), 'magenta'))
        if self.round == node.round:
            if self.isPrinter():
                print(colored("rounds correct, adding item to tree " + str(self.round), 'green'))
                # check if tree contains parent node (parent node would not be in the tree if it came in after timeout)
            if self.tree.contains(node.getGrandparentsString()) == False:
                # if parent node is not in the tree, add it with value of None
                print("adding None 1: " + str(node.getGrandparentsString()))
                newParents = node.parents[:-1]
                newVal = None
                newNode = EIGNode(newVal, newParents, self.round-1)
                self.tree.create_node(node.getGrandparentsString(), node.getGrandparentsString(), parent=node.getGreatGrandparentsString(), data=newNode)
            self.tree.create_node(node.getParentsString(), node.getParentsString(), parent=node.getGrandparentsString(), data=node)
        else:
            if self.isPrinter():
                print(colored("rounds incorrect, adding None val " + str(self.round), 'red'))

                    # print("adding None 2: " + str(node.getParentsString()))
                    # # if parent node is not in the tree, add it with value of None
                    # newParents = node.parents[:]
                    # newVal = None
                    # newNode = EIGNode(newVal, newParents, self.round)
                    # self.tree.create_node(node.getParentsString(), node.getParentsString(), parent=node.getGrandparentsString(), data=newNode)
            network.log.debug(str(self) + " missed input in round " + str(self.round) + " from " + str(sender))
            network.log.debug(str(node))

    def addMissedNodes(self, network):
        allNodes = []
        for node in self.tree.nodes.values():
            allNodes.append(node)
        for item in allNodes:
            newParents = item.data.getParents()
            if self.tree.depth(item) == self.round:
                for otherNode in network.getProcesses():
                    thisParents = copy.copy(newParents)
                    if self.round == 0:
                        thisParents = []
                    if (otherNode != self) & (otherNode not in thisParents):
                        thisParents.append(otherNode)
                        thisParentsString = listToString(thisParents)
                        if (self.tree.contains(thisParentsString) == False):
                            newVal = None
                            newNode = EIGNode(newVal, thisParents, self.round)
                            self.tree.create_node(thisParentsString, thisParentsString, parent=item, data=newNode)


    # increment round, add missed EIG nodes, update drift, call sendToAll
    def timeout(self, network):
        if self.isPrinter():
            print(colored("timed out for round " + str(self.round), 'blue'))
        network.log.debug(str(self) + "ended round: " + str(self.round))
        self.updateDrift()  # TODO: drift only updates at the end of each round (this is probably fine)
        self.addMissedNodes(network)
        self.round += 1
        self.sendToAll(network)

## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, gsr, val):
        Process.__init__(self, name, gsr)
        self.initialValue = val
        self.tree = self.initializeTree()
        self.currentLevel = []  # for building levels of tree before updating main tree

    def isHonest(self):
        return True

    def isPrinter(self):
        return False

    def initializeTree(self):
        tree = Tree()
        node = EIGNode(self.initialValue, [self], 0)
        tree.create_node("root", "root", data=node)
        return tree

    # Enqueues one receive event for every other process
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
                delay = self.drift + latency
                network.addToQueue(event, delay)

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        numNonNoneDecisionVals = 0
        for val in self.decisionVector:
            if val != None:
                numNonNoneDecisionVals +=1
        if numNonNoneDecisionVals > threshold:
            newGuess = getSmallestMostFrequentVal(self.decisionVector, allowNone=False)
            self.initialValue = newGuess
        self.tree = self.initializeTree(self.initialValue)
        self.decisionVector = []
        self.round = 0


## Byzantine Node ##

class ByzantineProcess(Process):

    def __init__(self, name, gsr, range):
        Process.__init__(self, name, gsr)
        self.range = range
        self.initialValue = self.getRandomValFromRange()
        self.tree = self.initializeTree(self.initialValue)
        self.currentLevel = []  # for building levels of tree before updating main tree

    def isHonest(self):
        return False

    def isPrinter(self):
        return False

    def initializeTree(self, rootVal):
        tree = Tree()
        node = EIGNode(self.initialValue, [self], 0)
        tree.create_node("root", "root", data=node)
        return tree

    def getRandomValFromRange(self):
        return random.randint(self.range[0], self.range[1])

    # Enqueues one receive event for every other process, but with random vals from range
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                newVal = self.getRandomValFromRange()
                newNode = EIGNode(newVal, node.getParents(), (self.round))
                event = ReceiveEvent(self, receiver, newNode, network)
                latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
                delay = self.drift + latency
                network.addToQueue(event, delay)

    # For Alg2. Randomize initialValues, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        self.initialValue = self.getRandomValFromRange()
        self.tree = self.initializeTree(self.initialValue)
        self.decisionVector = []
        self.round = 0


## FOR DEBUGGING ##
## Honest Printer Process ##

class HonestPrinterProcess(Process):

    def __init__(self, name, gsr, val):
        Process.__init__(self, name, gsr)
        self.initialValue = val
        self.tree = self.initializeTree(self.initialValue)
        print("Honest printer process: " + self.name + " initiated.")
        print("Initial value = " + str(self.initialValue))

    def isHonest(self):
        return True

    def isPrinter(self):
        return True

    def initializeTree(self):
        tree = Tree()
        node = EIGNode(self.initialValue, [self], 0)
        tree.create_node("root", "root", data=node)
        tree.show()
        return tree

    # Enqueues one receive event for every other process
    def broadcast(self, node, network):
        print(colored("Broadcasting node: " + str(node), 'blue'))
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
                delay = self.drift + latency
                print(colored("Adding event to queue: " + str(event), 'blue'))
                print(colored("Event has delay of: " + str(delay), 'blue'))
                print("global time: ", network.getGlobalTime())
                network.addToQueue(event, delay)

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        print(colored("Ending MicroRound", 'blue'))
        numNonNoneDecisionVals = 0
        for val in self.decisionVector:
            if val != None:
                numNonNoneDecisionVals +=1
        if numNonNoneDecisionVals > threshold:
            newGuess = getSmallestMostFrequentVal(self.decisionVector, allowNone=False)
            self.initialValue = newGuess
            print(colored("Updating initialValue to: " + newGuess, 'green'))
        else:
            print(colored("Could not update initialValue", 'red'))
        self.tree = self.initializeTree(self.initialValue)
        self.decisionVector = []
        self.round = 0

