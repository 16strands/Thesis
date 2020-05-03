###################
## Event Classes ##
###################

class GlobalEvent:

    def __init__(self, sender, network):
        self.sender = sender
        self.network = network

    def dispatch(self):
        raise NotImplementedError("dispatch must be implemented in the subclasses")

# Receive event to trigger receiver to update tree with new val
class ReceiveEvent(GlobalEvent):
    def __init__(self, sender, receiver, message, network):
        GlobalEvent.__init__(self, sender, network)
        self.receiver = receiver
        self.message = message

    # def __str__(self):
    #     return "ReceiveEvent(" + str(self.message) + ") from: " + str(self.sender.name) + " to: " + str(self.receiver.name)

    def __str__(self):
        return "ReceiveEvent(from: " + str(self.sender.name) + " to: " + str(self.receiver.name) + ")"

    def dispatch(self):
        self.receiver.receive(self.sender, self.message, self.network)

# Timeout event to trigger moving to the next round, updating the tree, and sendToAll-ing
class TimeoutEvent(GlobalEvent):
    def __init__(self, sender, network):
        GlobalEvent.__init__(self, sender, network)

    def __str__(self):
        return "TimeoutEvent(" + str(self.sender.name) + ")"

    def dispatch(self):
        self.sender.timeout(self.network)

# Beginning event to trigger the rest of the protocol
class BeginEIGEvent(GlobalEvent):
    def __init__(self, network):
        GlobalEvent.__init__(self, None, network)

    def __str__(self):
        return "BeginEvent"

    def dispatch(self):
        for process in self.network.getProcesses():
            process.sendToAll(self.network)

# Ending event to return decision vectors to main simulation
class DecisionEvent(GlobalEvent):
    def __init__(self, sender, decisionVector, network):
        GlobalEvent.__init__(self, sender, network)
        self.decisionVector = decisionVector

    def __str__(self):
        return "DecisionEvent(" + str(self.decisionVector) + ") from: " + str(self.sender.name)

    def dispatch(self):
        return (self.sender, self.sender.isHonest(), self.decisionVector)

# Beginning event to trigger stage 2 of EIG-Wrapper
class Stage2BeginEvent(GlobalEvent):
    def __init__(self, network):
        GlobalEvent.__init__(self, None, network)

    def __str__(self):
        return "Stage2BeginEvent"

    def dispatch(self):
        for process in self.network.getProcesses():
            process.stage2broadcast(self.network)

# Receive event to trigger receiver to update tree with new val
class Stage2ReceiveEvent(GlobalEvent):
    def __init__(self, sender, receiver, message, network):
        GlobalEvent.__init__(self, sender, network)
        self.receiver = receiver
        self.message = message

    # def __str__(self):
    #     return "ReceiveEvent(" + str(self.message) + ") from: " + str(self.sender.name) + " to: " + str(self.receiver.name)

    def __str__(self):
        return "Stage2ReceiveEvent(from: " + str(self.sender.name) + " to: " + str(self.receiver.name) + "), value = " + str(self.message)

    def dispatch(self):
        self.receiver.receiveStage2(self.message)

# Timeout event to trigger moving to the next round, updating the tree, and sendToAll-ing
class Stage2TimeoutEvent(GlobalEvent):
    def __init__(self, sender, network):
        GlobalEvent.__init__(self, sender, network)

    def __str__(self):
        return "Stage2TimeoutEvent(" + str(self.sender.name) + ")"

    def dispatch(self):
        self.sender.stage2timeout(self.network)

# event to trigger end of stage 2 for EIG-Wrapper
class Stage2EndEvent(GlobalEvent):
    def __init__(self, network):
        GlobalEvent.__init__(self, None, network)

    def __str__(self):
        return "Stage2EndEvent"

    def dispatch(self):
        decisions = []
        for process in self.network.getProcesses():
            decisions.append(process.stage2decide(self.network))
        return decisions
