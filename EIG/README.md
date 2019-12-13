NOTES 
---
* could have different "modes" for what buttons we're trying to push/what params we're testing
    - e.g. probability based (can we determine how many adversaries there are by measuring round complexity?)
    - could take in params in the command line 
    - or define the num of total honest and faulty nodes
* make log file for debugging 


QUESTIONS
---
### Priority Queue 
* How do I step through time?
    - priority queue won't wait between items, so there is no passing of time really
    - queue things to happen in between events to account for the passing of time? (like if the latency is 200, then either 200 events, or one type of event that "sleeps" for 200 ms?)
* Who should keep track of the event buffer? (aka is it global or separate for each node)
* Is the latency constant? 
    - does each node have its own ever-changing latency?
* how to make the queue simulate asynchrony?
    - start with varying latencies and make them converge after a certain point?
* has a timeout counter and then assumed "bot"
    - where to enter timeout thing?
* Is priority queue the right move? Maybe just a list that's ordered by the time specified? 
    - (but maybe priority queue is ok if it can simulate multiple events triggering at the same time)
    - (apparently they're served in the order they appear, but maybe that's good enough)
* When to add timeout events to the queue? After each send?


### General
* Use SimPy ?
* How to actually measure the stuff?
* What stuff am I measuring?
    - worst case running time when everyone is honest
    - what things can be tweaked for speed boost
    - failures vs byzantine failures
    - how do logical vs random adversaries affect speed?
    - how can we achieve worst case bound
* Byzantine processes sending different vals to every process? Or just one wrong val?
    - diff to each 


### EIG Tree
* store accumulated vals (for each round) in list until all messages in round received then enter in EIG tree?
* "eig as subroutine might be weird but gotta do it"
* Should byz nodes even keep track of a tree?
    - maybe if they're logical?
