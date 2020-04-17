#####################
## Process classes ##
#####################


## Imports ##

import random
from eigTree import EIGNode, EIGTree
from event import ReceiveEvent, TimeoutEvent, DecisionEvent
from termcolor import colored
from treelib import Tree

## Constants ##

LATENCY_MAX = 1.0
TIMEOUT = 20.0 # TODO figure out good timeout number
DRIFT = 0

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
    #
    # def __repr__(self):
    #     return str(self.name)

    # prints name, round, and drift
    def __repr__(self):
        return str(self.name) + ", " + str(self.round) + ", " + str(self.drift)

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
            delay = self.drift + random.uniform(0, LATENCY_MAX)
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
                val = self.getSmallestMostFrequentVal(vals, threshold=len(network.getProcesses()) - len(child.data.getParents()) - network.getMaxByz())
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
            decisionVector.append(decision)
        print("deciiosnVector" + str(decisionVector))
        print("length of decision vector: " + str(len(decisionVector)))
        print("expected length: " + str(numOtherProcesses))
        assert(len(decisionVector) == numOtherProcesses)
        self.decisionVector = decisionVector

    # receive incoming node and add to current level of tree
    def receive(self, sender, node, network):
        if self.isPrinter():
            print(colored("receiving event from " + str(sender) + " in round " + str(self.round), 'magenta'))
        if self.round == node.round:
            if self.isPrinter():
                print(colored("rounds correct, adding item to tree " + str(self.round), 'green'))
            # print(node.getParentsString())
            # print(node.getParentParentsString())
            self.tree.create_node(node.getParentsString(), node.getParentsString(), parent=node.getParentParentsString(), data=node)
        else:
            if self.isPrinter():
                print(colored("rounds incorrect, ignoring " + str(self.round), 'red'))
            network.log.debug(str(self) + " missed input in round " + str(self.round) + " from " + str(sender))
            network.log.debug(str(node))
    #
    # def getEIGRoot(self):
    #     print("getEIGROot")
    #     print(str(self.tree.get_node("root")))
    #     return self.tree.get_node("root")

    # increment round, update EIG tree, update drift, call sendToAll
    def timeout(self, network):
        if self.isPrinter():
            print(colored("timed out for round " + str(self.round), 'blue'))
        network.log.debug(str(self) + "ended round: " + str(self.round))
        self.updateDrift()  # TODO: drift only updates at the end of each round
        self.round += 1
        self.sendToAll(network)

    def getSmallestMostFrequentVal(self, vals, threshold=0):
        repeated = {}
        for val in vals:
            if val in repeated:
                repeated[val] += 1
            else:
                repeated[val] = 1
        if self.isPrinter():
            print(colored(repeated, 'yellow'))
        mostFrequent = (None, 0)
        for val in repeated.keys():
            if repeated[val] > mostFrequent[1]:
                mostFrequent = (val, repeated[val])
        if (mostFrequent[1] >= threshold):
            return mostFrequent[0]
        else:
            return None

## Honest Process ##

class HonestProcess(Process):

    def __init__(self, name, gsr, val):
        Process.__init__(self, name, gsr)
        self.initialValue = val
        self.tree = self.initializeTree(self.initialValue)
        self.currentLevel = []  # for building levels of tree before updating main tree

    def isHonest(self):
        return True

    def isPrinter(self):
        return False

    def initializeTree(self, rootVal):
        tree = Tree()
        node = EIGNode(self.initialValue, [self], 0)
        tree.create_node("root", "root", data=node)
        return tree

    # Enqueues one receive event for every other process
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                event = ReceiveEvent(self, receiver, node, network)
                delay = self.drift + random.uniform(0, LATENCY_MAX)
                network.addToQueue(event, delay)
            # else:
            #     print("yay!215")

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, network):
        numNonNoneDecisionVals = 0
        for val in self.decisionVector:
            if val != None:
                numNonNoneDecisionVals +=1
        if numNonNoneDecisionVals > network.tThreshold:
            newGuess = self.getSmallestMostFrequentVal(self.decisionVector)
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
        return random.randint(self.range[0], self.range[0])

    # Enqueues one receive event for every other process, but with random vals from range
    def broadcast(self, node, network):
        for receiver in network.getProcesses():
            if receiver not in node.getParents():
                newVal = self.getRandomValFromRange()
                newNode = EIGNode(newVal, node.getParents(), (self.round))
                event = ReceiveEvent(self, receiver, newNode, network)
                delay = self.drift + random.uniform(0, LATENCY_MAX)
                network.addToQueue(event, delay)
            # else:
            #     print("yay!byz")

    # For Alg2. Randomize initialValues, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, network):
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

    def initializeTree(self, rootVal):
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
                delay = self.drift + random.uniform(0, LATENCY_MAX)
                print(colored("Adding event to queue: " + str(event), 'blue'))
                print(colored("Event has delay of: " + str(delay), 'blue'))
                print("global time: ", network.getGlobalTime())
                network.addToQueue(event, delay)
            # else:
            #     print("yay!")

    # For Alg2. Update initialValue if applicable, reset tree, currentLevel, decisionVector, and round
    def endMicroRound(self, network):
        print(colored("Ending MicroRound", 'blue'))
        numNonNoneDecisionVals = 0
        for val in self.decisionVector:
            if val != None:
                numNonNoneDecisionVals +=1
        if numNonNoneDecisionVals > network.tThreshold:
            newGuess = self.getSmallestMostFrequentVal(self.decisionVector)
            self.initialValue = newGuess
            print(colored("Updating initialValue to: " + newGuess, 'green'))
        else:
            print(colored("Could not update initialValue", 'red'))
        self.tree = self.initializeTree(self.initialValue)
        self.decisionVector = []
        self.round = 0

