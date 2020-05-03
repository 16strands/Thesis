# a better way to command line test
import simulator
import argparse

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
            print("\nSimulator object initialized with " + str(self.numHonestProcessors) + " honest and " + str(self.numByzProcessors) + " byzantine process.")

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
        numHonestDecisionErrors = 0
        numByzDecisionErrors = 0
        firstDecisionVector = honestDecisions[0][1]
        for processor in honestDecisions:
            if len(processor[1]) != self.numProcessors:
                numHonestDecisionErrors += 1
            elif processor[1] !=  firstDecisionVector:
                numHonestDecisionErrors += 1
        for processor in byzantineDecisions:
            if len(processor[1]) != self.numProcessors:
                numByzDecisionErrors += 1
        if (numHonestDecisionErrors == 0) & (numByzDecisionErrors == 0):
            print("All honest decision vectors are equal and of the correct length.")
        else:
            print("Decision vectors incorrect.")
            if (self.numByzProcessors >= (self.numProcessors//3)):
                print("Too many byzantine processes.")
            print("Showing decision vectors...\n")
            self.showDecisions()
        print(str(self.sim.getMaxByz() + 1) + " rounds completed in " + str(round(self.sim.globalTime, 3)) + "ms")
        print("\nCONSENSUS REQUIREMENTS")
        print("Termination:  SUCCESS")
        if (numHonestDecisionErrors == 0) & (numByzDecisionErrors == 0):
            print("Agreement:    SUCCESS")
            print("Validity:     SUCCESS")
            print("\nConsensus reached!")
        else:
            print("Agreement:    FAIL")
            print("Validity:     FAIL")

        return self

    def testEIGWrapper(self):
        decisions = self.sim.runEIGWrapper()
        print(decisions)

    def showTree(self, process = 0, showValsOnly = True):
        print("Showing (" + str(self.sim.getProcesses()[process]) + ")'s tree")
        if showValsOnly:
            self.sim.getProcesses()[process].tree.show(data_property =  "val")
        else:
            self.sim.getProcesses()[process].tree.show()

    def showDecisions(self):
        print("HONEST DECISION VECTORS")
        for process in self.honestDecisions:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print("BYZANTINE DECISION VECTORS")
        for process in self.byzantineDecisions:
            print("Process: " + str(process[0]) + ", Decision Vector: " + str(process[1]))
        print()

if __name__ == "__main__":
    test = Tester(numHonest, numByz, printer, eventTrace, logger)
    test.testEIGWrapper()
