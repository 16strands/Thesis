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
from numpy import random
from event import BeginEIGEvent, TimeoutEvent, ReceiveEvent, DecisionEvent, Stage2BeginEvent, Stage2EndEvent, Stage2ReceiveEvent
from termcolor import colored

## CONSTANTS ##

START_VAL_HONEST = 5
VAL_RANGE = (0,1)

## SKEW ##

SKEW_RANGE = (0,1000000)
CORRECTION_RATE_RANGE = (0,1)

## SIMULATOR ##

class Simulator:

    def __init__(self, numHonest=11, numByzantine=5, printer=False, event_trace=False, logger=False):
        self.event_trace = event_trace
        self.logger = logger
        if logger:
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
        # initialize global time
        self.globalTime = 0.0
        # calculate maximum tolerated byzantine processes
        self.total_count = len(self.processes)
        self.maxByz = (self.total_count-1)//3
        self.maxByzWrapper = (self.total_count-1)//5
        # set thresholds for alg2
        self.tThreshold = (2*(self.total_count + self.maxByzWrapper))//3
        self.eThreshold = self.tThreshold

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
            skew = random.uniform(SKEW_RANGE[0], SKEW_RANGE[1])
            correctionRate = random.uniform(CORRECTION_RATE_RANGE[0], CORRECTION_RATE_RANGE[1])
            honestProcesses.append(process.HonestProcess(processName, skew, correctionRate, START_VAL_HONEST))
        if self.logger:
            self.log.debug(str(len(honestProcesses)) + " honest processes initiated")
        return honestProcesses

    # initialize honest printer processes
    def __initHonestPrinterProcess(self):
        honestPrinterProcesses = []
        processName = "printer"
        skew = random.uniform(SKEW_RANGE[0], SKEW_RANGE[1])
        correctionRate = random.uniform(CORRECTION_RATE_RANGE[0], CORRECTION_RATE_RANGE[1])
        honestPrinterProcesses.append(process.HonestPrinterProcess(processName, skew, correctionRate, START_VAL_HONEST))
        if self.logger:
            self.log.debug("Printer process initiated")
        return honestPrinterProcesses

    # initialize byzantine processes
    def __initByzProcesses(self, numByz):
        byzantineProcesses = []
        for i in range(numByz):
            processName = "byz" + str(i)
            skew = random.uniform(SKEW_RANGE[0], SKEW_RANGE[1])
            correctionRate = random.uniform(CORRECTION_RATE_RANGE[0], CORRECTION_RATE_RANGE[1])
            byzantineProcesses.append(process.ByzantineProcess(processName, skew, correctionRate, VAL_RANGE))
        if self.logger:
            self.log.debug(str(len(byzantineProcesses)) + " byzantine processes initiated")
        return byzantineProcesses

    # run eig protocol
    def runEIGProtocol(self):
        if self.logger:
            self.log.debug("Running EIG protocol")
        # initialize decision vectors
        honestDecisions = []
        byzDecisions = []
        # create beginning event and add to queue
        beginEvent = BeginEIGEvent(self)
        self.addToQueue(beginEvent, 0)
        # dispatch events in eventQueue until it is empty
        while len(self.eventQueue) > 0:
            # pop time and event
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
            # set global time to the time of each event as it is popped off the queue
            self.globalTime = t
            # dispatch event
            decision = e.dispatch()
            if decision:
                if decision[1] == True:
                    honestDecisions.append([decision[0], decision[2]])
                else:
                    byzDecisions.append([decision[0], decision[2]])
        if self.logger:
            self.log.debug("HONEST DECISION VECTORS: " + str(honestDecisions))
            self.log.debug("BYZANTINE DECISION VECTORS: " + str(byzDecisions))
            self.log.debug("EIG protocol finished")
        return (honestDecisions, byzDecisions)

    def getProcesses(self):
        return self.processes

    def addToQueue(self, event, t):
        heapq.heappush(self.eventQueue, (t + self.globalTime, id(event), event))

    def getMaxByz(self):
        return self.maxByz

    def getGlobalTime(self):
        return self.globalTime

    def showDecisions(self, decs):
        print("HONEST DECISION VECTORS")
        for process in decs[0]:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print("BYZANTINE DECISION VECTORS")
        for process in decs[1]:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print()

    def runEIGWrapper(self):
        if self.logger:
            self.log.debug("Running ALG 2 protocol")
        decided = False
        decisions = {}
        phi = 0
        while decided != True:
            phi += 1
            print("running EIG")
            # Stage 1
            self.runEIGProtocol()
            for process in self.getProcesses():
                process.endMicroRound(self.tThreshold)
            # Stage 2
            stage2BeginEvent = Stage2BeginEvent(self)
            self.addToQueue(stage2BeginEvent, self.globalTime)
            while len(self.eventQueue) > 0:
                # pop time and event
                t, _, e = heapq.heappop(self.eventQueue)
                self.globalTime = t
                e.dispatch()
            stage2EndEvent = Stage2EndEvent(self)
            self.addToQueue(stage2EndEvent, self.globalTime)
            while len(self.eventQueue) > 0:
                # pop time and event
                t, _, e = heapq.heappop(self.eventQueue)
                self.globalTime = t
                potentialDecisions = e.dispatch()
                if potentialDecisions:
                    for process in potentialDecisions:
                        if process[0] == True:
                            decisions[process[2]] = process[1]
            print(decisions)
            if len(decisions) == len(self.getProcesses()):
                decided = True
        print("Phi: " + str(phi))
        return decisions

# if __name__ == '__main__':
#     sim = Simulator()
#     cProfile.runctx('sim.runEIGProtocol()', globals(), locals())