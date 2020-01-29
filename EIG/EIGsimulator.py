###################
## EIG Simulator ##
###################

# Main code for running the simulation

## IMPORTS ## 

import process
from pqueue import PriorityQueue
from numpy import random
import logging

## CONSTANTS ##

HONEST_COUNT = 4
BYZ_COUNT = 1
# CRASHED_COUNT = 0 # could check to make sure it's also crash tolerant
START_VAL_HONEST = 0
TOTAL_COUNT = BYZ_COUNT + HONEST_COUNT
MAX_TOLERATED_BYZ = int(TOTAL_COUNT / 3) + 1  # TODO: check this math lol
VAL_RANGE = (0, 30)
START_LATENCY_MAX = 500
TIMEOUT = 200  # time after current time that timeout will be executed
EVENT_TRACE = True # enable for verbose mode
GSR = 5


## SIMULATOR ##

class EIGSimulator:

    def __init__(self):
        self.log = self.__setUpLogger()
        self.byzProcesses = self.__initByzProcesses()
        self.honestProcesses = self.__initHonestProcesses()
        self.eventQueue = PriorityQueue()
        self.processes = self.honestProcesses + self.byzProcesses
        self.round = 1
        self.latencyMax = 500
        # self.latencyMax = START_LATENCY_MAX / (self.round + 1) # TODO: Make this dependent on GSR

    def __setUpLogger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('simulator.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def __initHonestProcesses(self):
        honestProcesses = []
        for i in range(HONEST_COUNT):
            processName = "p" + str(i)
            honestProcesses.append(process.HonestProcess(processName, START_VAL_HONEST))
        self.log.debug("Honest processes initiated")
        return honestProcesses

    def __initByzProcesses(self):
        byzantineProcesses = []
        for i in range(BYZ_COUNT):
            processName = "byz" + str(i + HONEST_COUNT)
            byzantineProcesses.append(process.ByzantineProcess(processName, VAL_RANGE))
        self.log.debug("Byzantine processes initiated")
        return byzantineProcesses

    def runEIGProtocol(self):
        self.log.debug("Running EIG protocol")
        for r in range(MAX_TOLERATED_BYZ):
            self.executeRound(r)
        self.log.debug("EIG protocol finished")

    def executeRound(self, round):
        # Populate the event queue
        self.log.debug("Begin round " + str(self.getRoundNum()))
        for process in self.processes:
            latency = self.getProcessLatency()
            process.sendToAll(self, latency)
            # timeoutEvent = process.sendToAll(self, latency)
            # self.addToQueue(timeoutEvent, TIMEOUT)  # TODO: does this also need latency?  # I will wait 200ms for all my responses to come in
            self.log.debug(str(process) + "events added to queue")
        # Execute event queue
        self.log.debug("All events added to queue. Executing queue")
        print(self.eventQueue)
        while not self.eventQueue.isEmpty():
            e, t = self.eventQueue.pop()
            if EVENT_TRACE:
                print(str(e) + " at time " + str(t))
            self.log.debug("Dispatching " + str(e))
            e.dispatch()
        self.log.debug("Event queue executed")
        # Ask processes to update their trees
        for process in self.processes:
            self.log.debug("Updating tree for: " + str(process))
            process.updateTree()
        self.log.debug("End round " + str(self.getRoundNum()))
        self.round += 1

    # Weird way of calculating random latency but couldn't figure out a different way to have values more likely to be close to 0 but also stay within a predefined range
    def getProcessLatency(self):
        firstVal = random.rand()
        if firstVal < .5:
            return random.randint(0, self.latencyMax//4)
        elif firstVal < .75:
            return random.randint(0, self.latencyMax//2)
        else:
            return random.randint(0, self.latencyMax)

    def getProcesses(self):
        return self.processes

    def getEventQueue(self):
        return self.eventQueue

    def getRoundNum(self):
        return self.round

    def removeFromQueue(self, event):
        self.eventQueue.removeByEvent(event)

    def addToQueue(self, event, t):
        self.eventQueue.enqueue((event, t))



## Simple smoke test ##

def test():
    simulator = EIGSimulator()
    print("Honest Processes:")
    print(simulator.honestProcesses)
    print()
    print("Byzantine Processes:")
    print(simulator.byzProcesses)
    print()
    print("Total Processes:")
    print(simulator.processes)
    print()
    print("done")

def test2():
    sim = EIGSimulator()
    sim.runEIGProtocol()
    print(sim.getProcesses()[1].tree)