
class Process:
    def __init__(self, id, burstTime, meanInterIOInterval):
        self.id = id

        self.leftBurstTime = burstTime #execution time
        self.nextReadyTime = 0
        self.lastEndTime = 0

        self.meanInterIOInterval = meanInterIOInterval #The mean inter-I/O intervals for the jobs
        self.thisRunningTime = 0

        self.place = "start" #A job, once it enters the system, can be either in the Ready queue, or I/O Waiting queue, or it is being executed by the CPU

        self.turnaroundTime = 0
        self.runningTime = 0
        self.waitingTime = 0

        self.predictBurstTime = 0
