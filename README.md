## Simulating Byzantine Fault Tolerant Consensus Protocols on a Partially Synchronous Distributed System
#### An undergraduate thesis by Sarah Strand
###### Reed College Class of 2020

This is a simulated implementation of algorithms 1, 2, & 3 in the paper "A Leader-Free Byzantine Consensus Algorithm" by Fatemeh Borran and André Schiper (2011). Extended paper with appendices can be found [here](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.178.4470&rep=rep1&type=pdf "A Leader-Free Byzantine Consensus Algorithm").
______

## TODO (started 3/16/20)
- [x] Implement EIG
- [x] Implement global time
- [x] Allow for floats in eventQueue to prohibit simultaneous events
- [x] Have receive function add 'None' to tree when no value is received during that round
- [x] Order decision vectors correctly
- [ ] Verify that printerProcesses work the same as honestProcesses
- [x] Make test file (at least for easier command line testing)
- [x] Better estimation of realistic latencies
- [ ] Clock synchronization protocols probably exist, look at them to figure out how rounds are controlled
- [ ] GSR logic
- [x] Add something to check and report pass/fail of consensus requirements at the end of protocol for each process
- [x] Make processes compute decision vectors
- [x] Abstract EIG for use in algorithms 2 & 3
- [ ] Finish implementing Algorithm 2
- [ ] Implement Algorithm 3 (maybe)


## NOTES

#### Latency
Latency is modeled using a lognormal distribution because it looks about right. This is the code:
`(numpy.random.lognormal(0.8, 0.5))*10`
Use  [this](https://stackoverflow.com/questions/8870982/how-do-i-get-a-lognormal-distribution-in-python-with-mu-and-sigma "stackoverflow on how to plot this thing") to figure out how to generate a pdf and cdf.

#### Priority Queue
* how to make the queue simulate asynchrony?
    - start with varying drifts and make them converge after a certain point (gsr)


#### Possible Measurements
* worst case running time when everyone is honest
* what things can be tweaked for speed boost
* crash failures vs byzantine failures
* how do logical vs random adversaries affect speed?
* how can we achieve worst case bound
* can we determine how many adversaries there are by measuring number of rounds it takes to come to consensus?
     
     
## QUESTIONS
* GSR is established by setting a latency range at t=0 and then the range decreases until the GSR and then the range becomes 1 and the clocks are synchronized





