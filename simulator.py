###############
## Simulator ##
###############

# Main code for running the simulation

## IMPORTS ## 

import cProfile
import process
from random import shuffle
from numpy import random
import logging
import heapq
from event import BeginEvent

## CONSTANTS ##

HONEST_COUNT = 10
BYZ_COUNT = 2
TOTAL_COUNT = BYZ_COUNT + HONEST_COUNT
MAX_TOLERATED_BYZ = int(TOTAL_COUNT / 3) - 1

START_VAL_HONEST = 5
VAL_RANGE = (1, 1)

TIMEOUT = 200  # time after current time that timeout will be executed
GSR = 5  # TODO: implement global stabilization round

EVENT_TRACE = False # enable for verbose mode

## SIMULATOR ##

class Simulator:

    def __init__(self):
        # set up logger
        self.log = self.__setUpLogger()
        # initialize processes
        self.byzProcesses = self.__initByzProcesses()
        self.honestProcesses = self.__initHonestProcesses()
        self.processes = self.honestProcesses + self.byzProcesses
        # Randomize the list of processes just in case
        shuffle(self.processes)
        # set up event queue
        self.eventQueue = []
        heapq.heapify(self.eventQueue)

        self.globalTime = 0

    # set up logger
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

    # initialize honest processes
    def __initHonestProcesses(self):
        honestProcesses = []
        for i in range(HONEST_COUNT):
            processName = "p" + str(i)
            honestProcesses.append(process.HonestProcess(processName, GSR, START_VAL_HONEST))
        self.log.debug(str(len(honestProcesses)) + " honest processes initiated")
        return honestProcesses

    # initialize byzantine processes
    def __initByzProcesses(self):
        byzantineProcesses = []
        for i in range(BYZ_COUNT):
            processName = "byz" + str(i)
            byzantineProcesses.append(process.ByzantineProcess(processName, GSR, VAL_RANGE))
        self.log.debug(str(len(byzantineProcesses)) + " byzantine processes initiated")
        return byzantineProcesses

    # run eig protocol
    def runEIGProtocol(self):
        self.log.debug("Running EIG protocol")
        # initialize byzantine vectors for debugging
        honestDecisions = []
        byzDecisions = []
        # create beginning event and add to queue
        beginEvent = BeginEvent(self)
        self.addToQueue(beginEvent, 0)
        while len(self.eventQueue) > 0:
            t, _, e = heapq.heappop(self.eventQueue)
            if EVENT_TRACE:
                print(str(e) + " at time " + str(t))
            decision = e.dispatch()
            if decision:
                if decision[0] == True:
                    honestDecisions.append(decision[1])
                else:
                    byzDecisions.append(decision[1])
            self.globalTime = t  # TODO: fix this
            print(self.globalTime)
        self.log.debug("Event queue finished")
        self.log.debug("HONEST DECISION VECTOR: " + str(honestDecisions))
        self.log.debug("BYZANTINE DECISION VECTOR: " + str(byzDecisions))
        self.log.debug("EIG protocol finished")

    def getProcesses(self):
        return self.processes

    def getEventQueue(self):
        return self.eventQueue

    def addToQueue(self, event, t):
        heapq.heappush(self.eventQueue, (t + self.globalTime, id(event), event))

    def getMaxByz(self):
        return MAX_TOLERATED_BYZ

    def getGlobalTime(self):
        return self.globalTime



## Simple smoke tests ##

def test():
    simulator = Simulator()
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
    sim = Simulator()
    sim.runEIGProtocol()

# if __name__ == '__main__':
#     sim = Simulator()
#     cProfile.runctx('sim.runEIGProtocol()', globals(), locals())