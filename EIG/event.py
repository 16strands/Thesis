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
        print("DISPATCHING RECEIVE EVENT")
        self.receiver.receive(self.sender, self.message, self.network)


class TimeoutEvent(GlobalEvent):
    def __init__(self, sender, network):
        GlobalEvent.__init__(self, sender, network)

    def __str__(self):
        return "TimeoutEvent(" + str(self.sender) + ")"

    # def dispatch(self):
    #     print("DISPATCHING TIMEOUT EVENT")
    #     for item in self.network.eventQueue.pqueue:
    #         if item[0].sender == self.sender:
    #             print("REMOVING " + str(item) + " FROM QUEUE")
    #             self.network.removeFromQueue(item)

    def dispatch(self):
        print("DISPATCHING TIMEOUT EVENT")
        self.sender.timeout(self.network)


