########################
## EIG Simulator code ##
########################

## IMPORTS ## 

from node import Node, EIGNode
from random import randint
from pqueue import PriorityQueue

## CONSTANTS ##

HONEST_NODE_COUNT = 5
BYZ_NODE_COUNT = 1
# CRASHED_NODE_COUNT = 0 # could check to make sure it's also crash tolerant
START_VAL_HONEST = 0
TOTAL_NODES = BYZ_NODE_COUNT + HONEST_NODE_COUNT
MAX_TOLERATED_BYZ = int(TOTAL_NODES/3) + 1 # TODO: check this math lol
VAL_RANGE = (0,1)
# NETWORK_LATENCY = 200 # Or does each node have its own latency? 
# enqueue timeout after each send? like "if i dont receive anythign within 200ms then stoP?"


# Maybe not a proirity queue!!! Since things can actually happen at the same time!! 
# maybe just a list of lists ordered by the time specified ?? 
# OR MAYBE PRIORITY QUEUE CAN TRIGGER EVENTS AT THE SAME TIME IF THEY HAVE THE SAME PRIORITY
# no, apparently they're served in the order they appear, but maube that's good enough?
# but i can't code in the queue being timed bc everythign is gonna happen so fast 

## SIMULATOR ##

class EIGSimulator:

    def __init__(self):
        self.byzNodes = initByzNodes() 
        self.honestNodes = initHonestNodes()
        self.eventQueue = PriorityQueue()
        self.nodes = self.byzNodes + self.honestNodes

    def initHonestNodes():
        for i in range HONEST_NODE_COUNT:
            nodeName = "n"+str(i)
            honestNodes += Node(false, nodeName, START_VAL_HONEST)

    def initByzNodes():
        for i in range BYZ_NODE_COUNT:  # if I do it this way do i really need to note that it's byz or can it just be the same class but with a random value?
            byzVal = randint(VAL_RANGE[0], VAL_RANGE[1])
            nodeName = "n"+str(i+HONEST_NODE_COUNT)
            byzNodes += Node(True, i, byzVal)

    def runEIGProtocol():
        for r in range MAX_TOLERATED_BYZ:
            executeRound(r)

    def executeRound(round):
        for node in self.nodes:
            self.eventQueue.enqueue(node.broadcast()) ## add all broadcasts to queue
        for node in self.nodes:    
            node.receive()

