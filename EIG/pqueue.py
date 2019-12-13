###########################
## Simple Priority Queue ##
###########################

# Heavily inspired by geeksforgeeks

class PriorityQueue(object):
    def __init__(self):
        self.pqueue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.pqueue])


    def isEmpty(self):
        return len(self.pqueue) == 0


    def enqueue(self, item):
        self.pqueue.append(item)


    # for popping an element based on Priority
    def dequeue(self):
        try:
            max = 0
            for i in range(len(self.pqueue)):
                if self.pqueue[i] > self.pqueue[max]:
                    max = i
            item = self.pqueue[max]
            del self.pqueue[max]
            return item
        except IndexError:
            print()
            exit()