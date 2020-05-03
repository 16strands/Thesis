## Simulating Byzantine Fault Tolerant Consensus Protocols on a Partially Synchronous Distributed System
#### An undergraduate thesis by Sarah Strand
###### Reed College Class of 2020

This is a simulated implementation of algorithms 1 and 2 from the paper "A Leader-Free Byzantine Consensus Algorithm" by Fatemeh Borran and André Schiper (2011). Extended paper with appendices can be found [here](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.178.4470&rep=rep1&type=pdf "A Leader-Free Byzantine Consensus Algorithm").
Had I more time, I would have also implemented 3 and 4.
______

## TODO (started 3/16/20)
- [x] Implement EIG
- [x] Implement global time
- [x] Allow for floats in eventQueue to prohibit simultaneous events
- [x] Have receive function add 'None' to tree when no value is received during that round
- [x] Order decision vectors correctly
- [x] Verify that printerProcesses work the same as honestProcesses
- [x] Make test file (at least for easier command line testing)
- [x] Better estimation of realistic latencies
- [x] GSR logic
- [x] Add something to check and report pass/fail of consensus requirements at the end of protocol for each process
- [x] Make processes compute decision vectors
- [x] Abstract EIG for use in algorithms 2 & 3
- [x] Finish implementing Algorithm 2
- [ ] Optimize EIG (pre-initialize EIG trees)
- [ ] Fix global time for insane skew timing?


## NOTES

#### Latency
Latency is modeled using a lognormal distribution because it looks about right. This is the code:
`(numpy.random.lognormal(0.8, 0.5))*10`
Use  [this](https://stackoverflow.com/questions/8870982/how-do-i-get-a-lognormal-distribution-in-python-with-mu-and-sigma "stackoverflow on how to plot this thing") to figure out how to generate a pdf and cdf.


#### Possible Measurements
* worst case running time when everyone is honest
* what things can be tweaked for speed boost
* crash failures vs byzantine failures
* how do logical vs random adversaries affect speed?
* how can we achieve worst case bound
* can we determine how many adversaries there are by measuring number of rounds it takes to come to consensus?



