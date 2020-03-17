###########################
## Simple Min-Priority Queue ##
###########################

# Implementation of a priority queue for event queue #
# Items should be a list with 0th elt being the event and 1st elt being the priority
# Pops lowest priority first

# Heavily inspired by geeksforgeeks

class PriorityQueue(object):
    def __init__(self):
        self.pqueue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.pqueue])

    def __len__(self):
        return len(self.pqueue)

    def isEmpty(self):
        return len(self.pqueue) == 0

    def enqueue(self, item):
        self.pqueue.append(item)

    def removeByEvent(self, event):
        for item in self.pqueue:
            if item[0] == event:
                self.pqueue.remove(item)
                return
        raise LookupError("No such event")

    # for popping an element based on Priority
    def pop(self):
        try:
            min = 0
            for i in range(len(self.pqueue)):
                if self.pqueue[i][1] < self.pqueue[min][1]:
                    min = i
            item = self.pqueue[min]
            del self.pqueue[min]
            return item[0], item[1]
        except IndexError:
            print()
            exit()