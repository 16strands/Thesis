###########
## TESTS ##
###########

import simulator
import argparse

# parse command line args
parser = argparse.ArgumentParser(description='Test consensus protocols')
parser.add_argument('-p', '--printer', action='store_true',
    help="enable printer process")
parser.add_argument('-l', '--logger', action='store_true',
    help="enable logging")
parser.add_argument('-e', '--eventTrace', action='store_true',
    help="enable event trace")
parser.add_argument('-hp', type=int, default=5,
    help="Number of honest processes. Default 5")
parser.add_argument('-bp', type=int, default=2,
    help="Number of byzantine processes. Default 2")
args = parser.parse_args()

printer = args.printer
eventTrace = args.eventTrace
numHonest = args.hp
numByz = args.bp
logger = args.logger

class Tester():
    def __init__(self, numHonest, numByzantine, printer, eventTrace, logger):
        self.sim = self.trySimulator(numHonest, numByzantine, printer, eventTrace, logger)
        self.numHonestProcessors = len(self.sim.honestProcesses)
        self.numByzProcessors = len(self.sim.byzProcesses)
        self.numProcessors = len(self.sim.getProcesses())
        if printer:
            print("\nSimulator object initialized with " + str(self.numHonestProcessors) + " honest, " + str(self.numByzProcessors) + " byzantine, and 1 printer process.")
        else:
            print("\nSimulator object initialized with " + str(self.numHonestProcessors) + " honest and " + str(self.numByzProcessors) + " byzantine processes.")

    # try making a sim object with command line args
    def trySimulator(self, numHonest, numByzantine, printer, eventTrace, logger):
        sim = None
        try:
            sim = simulator.Simulator(numHonest=numHonest, numByzantine=numByzantine, printer=printer, event_trace=eventTrace, logger=logger)
        except:
            print("Error creating simulator")
        return sim

    def testEIG(self):
        print("\nRunning EIG...")
        honestDecisions, byzantineDecisions = self.sim.runEIGProtocol()
        print("Finished.")
        self.honestDecisions = honestDecisions
        self.byzantineDecisions = byzantineDecisions
        self.checkRequirements(honestDecisions)
        return self

    def testEIGWrapper(self):
        print("\nRunning EIG-Wrapper...")
        phi, decisions = self.sim.runEIGWrapper()
        self.wrapperDecisions = decisions
        print("Finished.")
        print(str(phi) + " rounds completed in " + str(round(self.sim.globalTime, 3)) + "ms")
        self.checkWrapperRequirements(decisions)
        return self

    # print process[0] tree in console
    def showTree(self, process = 0, showValsOnly = False, showParentsOnly = False):
        print("Showing (" + str(self.sim.getProcesses()[process]) + ")'s tree")
        if showValsOnly:
            self.sim.getProcesses()[process].tree.show(data_property =  "val")
        elif showParentsOnly:
            self.sim.getProcesses()[process].tree.show(data_property="parents")
        else:
            self.sim.getProcesses()[process].tree.show()

    # pretty print eig decision vectors
    def showDecisions(self):
        print("HONEST DECISION VECTORS")
        for process in self.honestDecisions:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print("BYZANTINE DECISION VECTORS")
        for process in self.byzantineDecisions:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print()

    # check eig consensus requirements
    def checkRequirements(self, decisions):
        validity = None
        termination = True # if we've gotten here it's terminated
        agreement = None
        firstDecisionVector = decisions[0][1]
        # check for agreement
        errors = 0
        for processor in decisions:
            if len(processor[1]) != self.numProcessors:
                errors += 1
            if processor[1] != firstDecisionVector:
                errors += 1
        if errors > 0:
            agreement = False
            print("Agreement failed.")
            if (self.numProcessors <= 3 * (self.numByzProcessors)):
                print("Too many byzantine processes.")
            print("Showing decision vectors...\n")
            self.showDecisions()
        else:
            agreement = True
        # check for validity
        initialValue = simulator.START_VAL_HONEST
        errors = 0
        for processor in decisions:
            repeated = {}
            for item in processor[1]:
                if item in repeated:
                    repeated[item] += 1
                else:
                    repeated[item] = 1
            mostFrequent = (None, 0)
            for val in repeated.keys():
                if repeated[val] > mostFrequent[1]:
                    mostFrequent = (val, repeated[val])
            if mostFrequent[0] != initialValue:
                errors += 1
        if errors > 0:
            validity = False
            print("Validity failed.")
        else:
            validity = True
        print(str(self.sim.getMaxByz() + 1) + " rounds completed in " + str(round(self.sim.globalTime, 3)) + "ms")
        self.printReport(termination, validity, agreement)

    # check eig-wrapper consensus requirements
    def checkWrapperRequirements(self, decisions):
        validity = None
        termination = True  # if we've gotten here it's terminated
        agreement = None
        decisionVals = list(decisions.values())
        firstDecision = decisionVals[0]
        # check agreement
        errors = 0
        if len(decisionVals) != self.numProcessors:
            print("here")
            errors += 1
        for processor in decisionVals:
            if processor != firstDecision:
                print("here2")
                errors += 1
        if errors > 0:
            agreement = False
            print("Agreement failed.")
            if (self.numProcessors <= 5 * (self.numByzProcessors)):
                print("Too many byzantine processes.")
            print("Showing decisions...\n")
            print(self.wrapperDecisions)
        else:
            agreement = True
        # check for validity
        initialValue = simulator.START_VAL_HONEST
        errors = 0
        for processor in decisionVals:
            if processor != initialValue:
                errors += 1
        if errors > 0:
            validity = False
            print("Validity failed.")
        else:
            validity = True
        self.printReport(termination, validity, agreement, wrapper=True)


    # pretty print consensus requirement results
    def printReport(self, termination, validity, agreement, wrapper=False):
        print("\nCONSENSUS REQUIREMENTS")
        if termination:
            print("Termination:  SUCCESS")
        else:
            print("Termination:  FAIL")
        if agreement:
            print("Agreement:    SUCCESS")
        else:
            print("Agreement:    FAIL")
        if validity:
            print("Validity:     SUCCESS")
        else:
            print("Validity:    FAIL")
        if termination & agreement & validity:
            print("\nConsensus reached!")
        else:
            print("\nConsensus failed.")
            if wrapper == False:
                decisionPrint = input("Show decisions? (y/n) ")
                if decisionPrint == 'y':
                    self.showDecisions()
                treePrint = input("Show tree? (y/n) ")
                if treePrint == 'y':
                    self.showTree()

if __name__ == "__main__":
    testRequested = input("EIG(1) or EIG-Wrapper(2)? ")
    test = Tester(numHonest, numByz, printer, eventTrace, logger)
    if testRequested == "1":
        test.testEIG()
    elif testRequested == "2":
        test.testEIGWrapper()
    else:
        print("Unrecognized command: " + testRequested)
