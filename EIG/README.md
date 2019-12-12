# NOTES 
* could have different "modes" for what buttons we're trying to push/what params we're testing
    - e.g. probability based (can we determine how many adversaries there are by measuring round complexity?)
    - could take in params in the command line 
    - or define the num of total honest and faulty nodes 


# QUESTIONS
* How do I step through time?
    - priority queue won't wait between items, so there is no passing of time really
        - queue things to happen in between events to account for the passing of time? (like if the latency is 200, then either 200 events, or one type of event that "sleeps" for 200 ms?)
        
        
# Who should keep track of the event buffer? (aka is it global or separate for each node)
# Is the latency constant? 
# SimPy ?
# How to actually measure the stuff?

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


# NETWORK_LATENCY = 200 # Or does each node have its own latency? 
# enqueue timeout after each send? like "if i dont receive anythign within 200ms then stoP?"


# Maybe not a proirity queue!!! Since things can actually happen at the same time!! 
# maybe just a list of lists ordered by the time specified ?? 
# OR MAYBE PRIORITY QUEUE CAN TRIGGER EVENTS AT THE SAME TIME IF THEY HAVE THE SAME PRIORITY
# no, apparently they're served in the order they appear, but maube that's good enough?
# but i can't code in the queue being timed bc everythign is gonna happen so fast 

