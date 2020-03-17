class GlobalEvent:

    def __init__(self, sender, network):
        self.sender = sender
        self.network = network

    def dispatch(self):
        raise NotImplementedError("dispatch must be implemented in the subclasses")


class ReceiveEvent(GlobalEvent):
    def __init__(self, sender, receiver, message, network):
        GlobalEvent.__init__(self, sender, network)
        self.receiver = receiver
        self.message = message

    def __str__(self):
        return "ReceiveEvent(" + str(self.message) + ") from: " + str(self.sender) + " to: " + str(self.receiver)


    def dispatch(self):
        self.receiver.receive(self.sender, self.message, self.network)


class TimeoutEvent(GlobalEvent):
    def __init__(self, sender, network):
        GlobalEvent.__init__(self, sender, network)

    def __str__(self):
        return "TimeoutEvent(" + str(self.sender) + ")"

    def dispatch(self):
        self.sender.timeout(self.network)


class BeginEvent(GlobalEvent):
    def __init__(self, network):
        GlobalEvent.__init__(self, None, network)

    def __str__(self):
        return "BeginEvent"

    def dispatch(self):
        for process in self.network.getProcesses():
            process.sendToAll(self.network)

class DecisionEvent(GlobalEvent):
    def __init__(self, sender, decision, network):
        GlobalEvent.__init__(self, sender, network)
        self.decision = decision

    def __str__(self):
        return "DecisionEvent(" + str(self.decision) + ") from: " + str(self.sender)

    def dispatch(self):
        return (self.sender.isHonest(), self.decision)

