# a better way to command line test
import simulator
import argparse

parser = argparse.ArgumentParser(description='Test consensus protocols')
parser.add_argument('-p', '--printer', action='store_true',
    help="enable printer process")
parser.add_argument('-e', '--eventTrace', action='store_true',
    help="enable event trace")
parser.add_argument('-hp', type=int, default=5,
    help="number of honest processes. default 5")
parser.add_argument('-bp', type=int, default=1,
    help="number of byzantine processes. default 1")
args = parser.parse_args()

printer = args.printer
eventTrace = args.eventTrace
numHonest = args.hp
numByz = args.bp

class Tester():
    def __init__(self, numHonest, numByzantine, printer, eventTrace):
        self.sim = self.trySimulator(numHonest, numByzantine, printer, eventTrace)
        self.numHonestProcessors = len(self.sim.honestProcesses)
        self.numByzProcessors = len(self.sim.byzProcesses)
        self.numProcessors = len(self.sim.getProcesses())
        if printer:
            print("Simulator object initialized with " + str(self.numHonestProcessors) + " honest, " + str(self.numByzProcessors) + " byzantine, and 1 printer process.")
        else:
            print("Simulator object initialized with " + str(self.numHonestProcessors) + " honest and " + str(self.numByzProcessors) + " byzantine process.")

    def trySimulator(self, numHonest, numByzantine, printer, eventTrace):
        sim = None
        try:
            sim = simulator.Simulator(numHonest=numHonest, numByzantine=numByzantine, printer=printer, event_trace=eventTrace)
        except:
            print("Error creating simulator")
        return sim

    def testEIG(self):
        honestDecisions, byzantineDecisions = self.sim.runEIGProtocol()
        numOtherProcesses = self.numProcessors - 1
        numHonestDecisionErrors = 0
        numByzDecisionErrors = 0
        for processor in honestDecisions:
            if len(processor[1]) != numOtherProcesses:
                numHonestDecisionErrors += 1
        for processor in byzantineDecisions:
            if len(processor[1]) != numOtherProcesses:
                numByzDecisionErrors += 1
        if (numHonestDecisionErrors == 0) & (numByzDecisionErrors == 0):
            print("All decision vector lengths are correct")
            print("EIG successful")
        else:
            print("Decision vector lengths incorrect")
            print("Number of incorrect honest processes:  " + str(numHonestDecisionErrors))
            print("Number of incorrect byzantine processes:  " + str(numByzDecisionErrors))
        return self

    def showTree(self, process = 0, showValsOnly = True):
        print("Showing (" + str(self.sim.getProcesses()[process]) + ")'s tree")
        if showValsOnly:
            self.sim.getProcesses()[process].tree.show(data_property =  "val")
        else:
            self.sim.getProcesses()[process].tree.show()

if __name__ == "__main__":
    test = Tester(numHonest, numByz, printer, eventTrace)
    test.testEIG()



