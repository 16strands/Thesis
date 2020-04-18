###############
## Simulator ##
###############

# Main code for running the simulation

## IMPORTS ## 

import cProfile
import process
from random import shuffle
import logging
import heapq
from event import BeginEvent, TimeoutEvent, ReceiveEvent, DecisionEvent
from termcolor import colored

## CONSTANTS ##

START_VAL_HONEST = 1
VAL_RANGE = (0,1)

TIMEOUT = 200  # time after current time that timeout will be executed
GSR = 5  # TODO: implement global stabilization round

# Parameters
E_THRESHOLD = 5
T_THRESHOLD = 5

## SIMULATOR ##

class Simulator:

    def __init__(self, numHonest=5, numByzantine=1, printer=False, event_trace=False):
        self.event_trace = event_trace
        # set up logger
        self.log = self.__setUpLogger()
        # initialize processes
        self.honestProcesses = self.__initHonestProcesses(numHonest)
        self.byzProcesses = self.__initByzProcesses(numByzantine)
        self.honestPrinterProcess = []
        if printer:
            self.honestPrinterProcess = self.__initHonestPrinterProcess()
        self.processes = self.honestProcesses + self.byzProcesses + self.honestPrinterProcess
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
    def __initHonestProcesses(self, numHonest):
        honestProcesses = []
        for i in range(numHonest):
            processName = "p" + str(i)
            honestProcesses.append(process.HonestProcess(processName, GSR, START_VAL_HONEST))
        self.log.debug(str(len(honestProcesses)) + " honest processes initiated")
        return honestProcesses

    # initialize honest printer processes
    def __initHonestPrinterProcess(self):
        honestPrinterProcesses = []
        processName = "printer"
        honestPrinterProcesses.append(process.HonestPrinterProcess(processName, GSR, START_VAL_HONEST))
        self.log.debug("Printer process initiated")
        return honestPrinterProcesses

    # initialize byzantine processes
    def __initByzProcesses(self, numByz):
        byzantineProcesses = []
        for i in range(numByz):
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
            if self.event_trace:
                if isinstance(e, TimeoutEvent):
                    print(colored(str(e) + " at time " + str(t), 'red'))
                elif isinstance(e, ReceiveEvent):
                    print(colored(str(e) + " at time " + str(t), 'blue'))
                elif isinstance(e, DecisionEvent):
                    print(colored(str(e) + " at time " + str(t), 'orange'))
                else:
                    print(str(e) + " at time " + str(t))
            self.globalTime = t
            decision = e.dispatch()
            if decision:
                if decision[1] == True:
                    honestDecisions.append([decision[0], decision[2]])
                else:
                    byzDecisions.append([decision[0], decision[2]])
        self.log.debug("HONEST DECISION VECTORS: " + str(honestDecisions))
        self.log.debug("BYZANTINE DECISION VECTORS: " + str(byzDecisions))
        self.log.debug("EIG protocol finished")
        return (honestDecisions, byzDecisions)

    def getProcesses(self):
        return self.processes

    def addToQueue(self, event, t):
        heapq.heappush(self.eventQueue, (t + self.globalTime, id(event), event))

    def getMaxByz(self):
        return (len(self.getProcesses())/3) - 1

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

# if __name__ == '__main__':
#     sim = Simulator()
#     cProfile.runctx('sim.runEIGProtocol()', globals(), locals())