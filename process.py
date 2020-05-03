#####################
## Process classes ##
#####################


## Imports ##

from eigNode import EIGNode
from event import ReceiveEvent, TimeoutEvent, DecisionEvent, Stage2ReceiveEvent, Stage2TimeoutEvent
from termcolor import colored
from treelib import Tree
import copy
from numpy import random

## Constants ##
TIMEOUT = 150.0 # TODO figure out good timeout number

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
    def __init__(self, name, skew, correctionRate):
        self.name = name
        self.round = 0
        self.skew = skew
        # correctionRate is number btwn 0,1 that determines how quickly the skew approaches zero. higher numbers correct quicker
        self.correctionRate = correctionRate
        self.decisionVector = []
        self.stage2received = []
        self.stage2timedout = False

    # uncomment desired repr method

    # prints name, init val
    # def __repr__(self):
    #     rep = "(Name: " + str(self.name) + ", InitVal: " + str(self.initialValue) + ") "
    #     return rep

    # only prints name

    def __repr__(self):
        return str(self.name)

    # prints name, round, and skew
    # def __repr__(self):
    #     return str(self.name) + ", " + str(self.round) + ", " + str(self.skew)

    def updateSkew(self):
        if self.skew > 0:
            self.skew = self.skew * (1-self.correctionRate)
        if self.skew <= 1:
            self.skew = 0

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
            delay = self.skew + latency
            network.addToQueue(decisionEvent, delay)
        # Otherwise broadcast and then add timeout event to queue
        else:
            if self.isPrinter():
                print(colored("sending to all round " + str(self.round), 'blue'))
            for node in self.tree.leaves():
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

            # add timeout event to queue
            timeoutEvent = TimeoutEvent(self, network)
            network.addToQueue(timeoutEvent, TIMEOUT + self.skew)
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
            val = getSmallestMostFrequentVal(vals)

            if val != None:
                return val
            else:
                if network.logger:
                    network.log.debug("No agreement on a value at this level.")
                if self.isPrinter():
                    print(colored("no agreement on value at this level of tree", 'red'))

    def decide(self, network):
        if self.isPrinter():
            print(colored("deciding " + str(self.round), 'blue'))
        decisionVector = []
        children = list(self.tree.children("root"))
        for child in children:
            decision = self.decideHelper(child, network)
            decisionVector.append((child.identifier, decision))
        decisionVector.sort()
        self.decisionVector = decisionVector

    # receive incoming node and add to current level of tree
    def receive(self, sender, node, network):
        if self.isPrinter():
            print(colored("receiving event from " + str(sender) + " in round " + str(self.round), 'magenta'))
        if len(node.getParents()) != len(set(node.getParents())):
            if network.logger:
                network.log.debug(str(self) + " ignoring node with repeated parents " + str(self.round) + " from " + str(sender))
                network.log.debug(str(node))
        elif self.round == node.round:
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
            if network.logger:
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
                    if (otherNode not in thisParents):
                        thisParents.append(otherNode)
                        thisParentsString =  listToString(thisParents)
                        if (self.tree.contains(thisParentsString) == False):
                            newVal = None
                            newNode = EIGNode(newVal, thisParents, self.round)
                            self.tree.create_node(thisParentsString, thisParentsString, parent=item, data=newNode)


    # increment round, add missed EIG nodes, update skew, call sendToAll
    def timeout(self, network):
        if self.isPrinter():
            print(colored("timed out for round " + str(self.round), 'blue'))
        if network.logger:
            network.log.debug(str(self) + "ended round: " + str(self.round))
        self.updateSkew()  # skew updates at the end of each round
        if self.isPrinter():
            print("UPDATED SKEW: ")
            print(self.skew)
        self.addMissedNodes(network)
        self.round += 1
        self.sendToAll(network)

    def stage2timeout(self, network):
        self.updateSkew()
        self.stage2timedout = True

    # for stage 2 of EIG-Wrapper
    def stage2broadcast(self, network):
        raise NotImplementedError("stage2broadcast method must be implemented by subclasses")

    def receiveStage2(self, message):
        if self.stage2timedout == False:
            self.stage2received.append(message)
        else:
            self.stage2received.append(None)

    def stage2decide(self, network):
        assert(len(self.stage2received) == len(network.getProcesses()))
        decision = getSmallestMostFrequentVal(self.stage2received, network.eThreshold, False)
        self.stage2received = []
        self.stage2timedout = False
        if decision != None:
            return (True, decision, self.name)
        else:
            return (False, None, self.name)


## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, skew, correctionRate, val):
        Process.__init__(self, name, skew, correctionRate)
        self.initialValue = val
        self.tree = self.initializeTree()

    def isHonest(self):
        return True

    def isPrinter(self):
        return False

    def initializeTree(self):
        tree = Tree()
        node = EIGNode(self.initialValue, [], 0)
        tree.create_node("root", "root", data=node)
        return tree

    # Enqueues one receive event for every other process
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            event = ReceiveEvent(self, receiver, node, network)
            latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
            delay = self.skew + latency
            network.addToQueue(event, delay)

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        numNonNoneDecisionVals = 0
        potentialVals = []
        for val in self.decisionVector:
            if val[1] != None:
                numNonNoneDecisionVals +=1
                potentialVals.append(val[1])
        if numNonNoneDecisionVals > threshold:
            newGuess = getSmallestMostFrequentVal(potentialVals, allowNone=False)
            self.initialValue = newGuess
        self.tree = self.initializeTree()
        self.decisionVector = []
        self.round = 0

    def stage2broadcast(self, network):
        for receiver in network.getProcesses():
            event = Stage2ReceiveEvent(self, receiver, self.initialValue, network)
            latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
            delay = self.skew + latency
            network.addToQueue(event, delay)
        timeout = Stage2TimeoutEvent(self, network)
        network.addToQueue(timeout, TIMEOUT+self.skew)


## Byzantine Node ##

class ByzantineProcess(Process):

    def __init__(self, name, skew, correctionRate, range):
        Process.__init__(self, name, skew, correctionRate)
        self.range = range
        self.initialValue = self.getRandomValFromRange()
        self.tree = self.initializeTree()

    def isHonest(self):
        return False

    def isPrinter(self):
        return False

    def initializeTree(self):
        tree = Tree()
        node = EIGNode(self.initialValue, [], 0)
        tree.create_node("root", "root", data=node)
        return tree

    def getRandomValFromRange(self):
        return random.randint(self.range[0], self.range[1])

    # Enqueues one receive event for every other process, but with random vals from range
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            newVal = self.getRandomValFromRange()
            newNode = EIGNode(newVal, node.getParents(), (self.round))
            event = ReceiveEvent(self, receiver, newNode, network)
            latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
            delay = self.skew + latency
            network.addToQueue(event, delay)

    # For Alg2. Randomize initialValues, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        self.initialValue = self.getRandomValFromRange()
        self.tree = self.initializeTree()
        self.decisionVector = []
        self.round = 0

    def stage2broadcast(self, network):
        for receiver in network.getProcesses():
            event = Stage2ReceiveEvent(self, receiver, self.getRandomValFromRange(), network)
            latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
            delay = self.skew + latency
            network.addToQueue(event, delay)
        timeout = Stage2TimeoutEvent(self, network)
        network.addToQueue(timeout, TIMEOUT + self.skew)


## FOR DEBUGGING ##
## Honest Printer Process ##

class HonestPrinterProcess(Process):

    def __init__(self, name, skew, correctionRate, val):
        Process.__init__(self, name, skew, correctionRate)
        self.initialValue = val
        self.tree = self.initializeTree()
        print("Honest printer process: " + self.name + " initiated.")
        print("Initial value = " + str(self.initialValue))

    def isHonest(self):
        return True

    def isPrinter(self):
        return True

    def initializeTree(self):
        tree = Tree()
        node = EIGNode(self.initialValue, [], 0)
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
                delay = self.skew + latency
                print(colored("Adding event to queue: " + str(event), 'blue'))
                print(colored("Event has delay of: " + str(delay), 'blue'))
                print("global time: ", network.getGlobalTime())
                network.addToQueue(event, delay)

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, threshold):
        print(colored("Ending MicroRound", 'blue'))
        numNonNoneDecisionVals = 0
        potentialVals = []
        for val in self.decisionVector:
            if val[1] != None:
                numNonNoneDecisionVals +=1
                potentialVals.append(val[1])
        if numNonNoneDecisionVals > threshold:
            newGuess = getSmallestMostFrequentVal(potentialVals, allowNone=False)
            self.initialValue = newGuess
            print(colored("Updating initialValue to: " + str(newGuess), 'green'))
        else:
            print(colored("Could not update initialValue", 'red'))
        self.tree.show(data_property =  "val")
        self.tree = self.initializeTree()
        self.decisionVector = []
        self.round = 0

    def stage2broadcast(self, network):
        for receiver in network.getProcesses():
            event = Stage2ReceiveEvent(self, receiver, self.initialValue, network)
            latency = (random.lognormal(0.8, 0.5)) * 10  # See README for latency explanation
            delay = self.skew + latency
            network.addToQueue(event, delay)
        timeout = Stage2TimeoutEvent(self, network)
        network.addToQueue(timeout, TIMEOUT + self.skew)
