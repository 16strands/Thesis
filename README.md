## Simulating Byzantine Fault Tolerant Consensus Protocols on a Partially Synchronous Distributed System
#### An undergraduate thesis by Sarah Strand
###### Reed College Class of 2020

This is a simulated implementation of algorithms 1, 2, & 3 in the paper "A Leader-Free Byzantine Consensus Algorithm" by Fatemeh Borran and André Schiper (2011). Extended paper with appendices can be found [here](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.178.4470&rep=rep1&type=pdf "A Leader-Free Byzantine Consensus Algorithm").
______

## TODO (started 3/16/20)
- [x] Implement EIG
- [x] Implement global time
- [x] Allow for floats in eventQueue to prohibit simultaneous events
- [ ] Better estimation of realistic latencies / clock drift logic
- [ ] Clock synchronization protocols probably exist, look at them to figure out how rounds are controlled
- [ ] GSR logic
- [ ] Add something to check and report pass/fail of consensus requirements at the end of protocol for each process
- [ ] Make processes compute decision vectors
- [ ] Abstract EIG for use in algorithms 2 & 3
- [ ] Implement Algorithm 2
- [ ] Implement Algorithm 3


## NOTES
---
#### Priority Queue 
* Stepping through time
    - priority queue won't wait between items, so there is no passing of time really
* how to make the queue simulate asynchrony?
    - start with varying latencies and make them converge after a certain point?
* has a timeout counter and then assumed None
* add timeouts to queue after broadcasting
    - "I've sent to all, now I will wait 200ms for all my responses to come in, else i'll assume None"


#### Possible Measurements
* worst case running time when everyone is honest
* what things can be tweaked for speed boost
* crash failures vs byzantine failures
* how do logical vs random adversaries affect speed?
* how can we achieve worst case bound
* can we determine how many adversaries there are by measuring number of rounds it takes to come to consensus?
     
     
## QUESTIONS
* Should the eventQueue be empty at the end of each round?
* GSR is established by setting a latency range at t=0 and then the range decreases until the GSR and then the range becomes 1 and the clocks are synchronized 
* What is a "micro-round" of EIG?





