NOTES 
---
* could have different "modes" for what buttons we're trying to push/what params we're testing
    - e.g. probability based (can we determine how many adversaries there are by measuring round complexity?)


QUESTIONS
---
### Priority Queue 
* How do I step through time?
    - priority queue won't wait between items, so there is no passing of time really
    - queue things to happen in between events to account for the passing of time? (like if the latency is 200, then either 200 events, or one type of event that "sleeps" for 200 ms?)
* Who should keep track of the event buffer? (aka is it global or separate for each node)
* how to make the queue simulate asynchrony?
    - start with varying latencies and make them converge after a certain point?
* has a timeout counter and then assumed None
* add timeouts to queue after broadcasting
    - "I've sent to all, now I will wait 200ms for all my responses to come in, else i'll assume None"


### General
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



EIG SIMulator has absolute time, event sheudling shoudl be priority queue qith key as time when it happens 
latency can be random generated with noise 
upon send, add recieve at the time it will offur -> look up latency and current time 

how to model local clock
    they use it for timeout 
    calculate next timeout based on previous timeout
    add in time for things to neve rbe processed out of order
    timeout method (end of round method for nodes, where theyd deicde tmoove on and treat everythign else as null)
    
asynchrony is that timtouts are all different / off
    maybe start off, wrong to begin with
    or get off later 
read realistic (real) literature on how this happens 

clock synchronization protocols probably exist, look at them to figure out how rounds are controlled 

maybe randomly generate a GSR -> genearte END OF ROUND signal for every party 

END OF ROUND FUNCTION separate from recieve
recieve store value in list (if we have them all, run END OF ROUND)
    
!!! add param for ^ !!!
    
figure out some model of how clocks get off 
     buggy?
     something happens?
     drift?
     
     
     
### NEW QUESTIONS
* Should the eventQueue be empty at the end of each round?
* GSR is established by setting a latency range at t=0 and then the range decreases until the GSR and then the range becomes 1 and the clocks are synchronized 