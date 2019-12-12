# NOTES 
* could have different "modes" for what buttons we're trying to push/what params we're testing
    - e.g. probability based (can we determine how many adversaries there are by measuring round complexity?)
    - could take in params in the command line 
    - or define the num of total honest and faulty nodes 


# QUESTIONS
* How do I step through time?
    - priority queue won't wait between items, so there is no passing of time really
        - queue things to happen in between events to account for the passing of time? (like if the latency is 200, then either 200 events, or one type of event that "sleeps" for 200 ms?)