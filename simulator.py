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
from event import BeginEvent, TimeoutEvent, ReceiveEvent, DecisionEvent
from termcolor import colored

## CONSTANTS ##

HONEST_COUNT = 10
BYZ_COUNT = 2
HONEST_PRINTER_COUNT = 0
TOTAL_COUNT = BYZ_COUNT + HONEST_COUNT + HONEST_PRINTER_COUNT
MAX_TOLERATED_BYZ = int(TOTAL_COUNT / 3) - 1

START_VAL_HONEST = 5
VAL_RANGE = (1, 1)

TIMEOUT = 200  # time after current time that timeout will be executed
GSR = 5  # TODO: implement global stabilization round

EVENT_TRACE = False # enable for verbose mode

# Parameters
E_THRESHOLD = 5
T_THRESHOLD = 5

## SIMULATOR ##

class Simulator:

    def __init__(self):
        # set up logger
        self.log = self.__setUpLogger()
        # initialize processes
        self.byzProcesses = self.__initByzProcesses()
        self.honestProcesses = self.__initHonestProcesses()
        self.honestPrinterProcesses = self.__initHonestPrinterProcesses()
        self.processes = self.honestProcesses + self.byzProcesses + self.honestPrinterProcesses
        # Randomize the list of processes just in case
        shuffle(self.processes)
        # set up event queue
        self.eventQueue = []
        heapq.heapify(self.eventQueue)

        self.globalTime = 0.0

        self.tThreshold = T_THRESHOLD
        self.eThreshold = E_THRESHOLD

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

    # initialize honest printer processes
    def __initHonestPrinterProcesses(self):
        honestPrinterProcesses = []
        for i in range(HONEST_PRINTER_COUNT):
            processName = "pp" + str(i)
            honestPrinterProcesses.append(process.HonestPrinterProcess(processName, GSR, START_VAL_HONEST))
        self.log.debug(str(len(honestPrinterProcesses)) + " honest processes initiated")
        return honestPrinterProcesses

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
        # dispatch events in eventQueue until it is empty
        while len(self.eventQueue) > 0:
            t, _, e = heapq.heappop(self.eventQueue)
            if EVENT_TRACE:
                if isinstance(e, TimeoutEvent):
                    print(colored(str(e) + " at time " + str(t), 'red'))
                elif isinstance(e, ReceiveEvent):
                    print(colored(str(e) + " at time " + str(t), 'blue'))
                elif isinstance(e, DecisionEvent):
                    print(colored(str(e) + " at time " + str(t), 'orange'))
                else:
                    print(str(e) + " at time " + str(t))
            # if isinstance(e, TimeoutEvent):
            #     print(str(e) + " at time " + str(t))
            self.globalTime = t
            decision = e.dispatch()
            if decision:
                if decision[1] == True:
                    honestDecisions.append([decision[0], decision[2]])
                else:
                    byzDecisions.append([decision[0], decision[2]])

            # if isinstance(e, TimeoutEvent):
            #     print(str(e))
            #     print(self.globalTime)
            # print(self.globalTime)
        self.log.debug("HONEST DECISION VECTORS: " + str(honestDecisions))
        self.log.debug("BYZANTINE DECISION VECTORS: " + str(byzDecisions))
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

    def runAlg2(self):
        self.log.debug("Running ALG 2 protocol")
        decided = False
        phi = 1
        while decided != True:
            self.runEIGProtocol()  # this seems very synchronous to wait until this completes to move on
            for process in self.processes:
                process.endMicroRound(self)








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