## QUESTIONS ##
# Who should keep track of the event buffer? (aka is it global or separate for each node)
# Is the latency constant? 
# SimPy
# How to actually measure the stuff?

class Node():
    def __init__(self, byz, name, val):
        self.byz = byz
        self.name = name # is this necessary?
        self.initialValue = val

    self.round = 0
    self.tree = {(root, initialValue)}

    def decide():
        pass

    def broadcast():  # return the value to be brodcasted
        pass
        #call some global function with sender, receiver and time as input, and latency
        # system call to send messages 

    def receive() : # event triggers at time specified at broadcast time 
    # store in list until all messageds in round received
    # then enter in EIG tree?
    #  has a timeout counter and then assumed "bot"
        # where to enter timeout thing?

    # eig as subroutine might be weird but gotta do it 
    # worst case running time when everyone is honest?
    # what things can be tweaked for speed boost?
    # how to make things asynchronous 
    # failures vs byzantine failures
    # how can byz failures slow this down? like logical adversaries
    # how can we achieve the worst case bound 
        

class EIGNode():
    def __init__(self, level, val, children):
        self.level = level
        self.val = val
        self.children = []


# make log file for debugging 

