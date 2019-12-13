###################
## EIG Simulator ##
###################

## IMPORTS ## 

import node
from pqueue import PriorityQueue

## CONSTANTS ##

HONEST_NODE_COUNT = 50
BYZ_NODE_COUNT = 10
# CRASHED_NODE_COUNT = 0 # could check to make sure it's also crash tolerant
START_VAL_HONEST = 0
TOTAL_NODES = BYZ_NODE_COUNT + HONEST_NODE_COUNT
MAX_TOLERATED_BYZ = int(TOTAL_NODES / 3) + 1  # TODO: check this math lol
VAL_RANGE = (0, 30)


# NETWORK_LATENCY = 200 # Or does each node have its own latency?
# enqueue timeout after each send? like "if i dont receive anythign within 200ms then stoP?"


## SIMULATOR ##

class EIGSimulator:

    def __init__(self):
        self.byzNodes = self.initByzNodes()
        self.honestNodes = self.initHonestNodes()
        self.eventQueue = PriorityQueue()
        self.nodes = self.honestNodes + self.byzNodes

    def initHonestNodes(self):
        honestNodes = []
        for i in range(HONEST_NODE_COUNT):
            nodeName = "n" + str(i)
            honestNodes.append(node.HonestNode(nodeName, START_VAL_HONEST))
        return honestNodes

    def initByzNodes(self):
        byzantineNodes = []
        for i in range(BYZ_NODE_COUNT):
            nodeName = "byz" + str(i + HONEST_NODE_COUNT)
            byzantineNodes.append(node.ByzantineNode(nodeName, VAL_RANGE))
        return byzantineNodes

    def runEIGProtocol(self):
        for r in range(MAX_TOLERATED_BYZ):
            self.executeRound(r)

    def executeRound(self, round):
        for node in self.nodes:
            self.eventQueue.enqueue(node.broadcast(round))  # add all broadcasts to queue
        for node in self.nodes:
            node.receive()


## Simple smoke test method ##

def test():
    simulator = EIGSimulator()
    print("Honest Nodes:")
    print(simulator.honestNodes)
    print()
    print("Byzantine Nodes:")
    print(simulator.byzNodes)
    print()
    print("Total nodes:")
    print(simulator.nodes)
    print()
    print("done")