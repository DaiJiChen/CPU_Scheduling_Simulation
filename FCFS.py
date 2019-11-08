from process import Process
from sort import sort
import numpy

# time unit : ms
class FCFS:
    def __init__(self):
        self.file = open("FCFS_output.txt", 'a')

        self.startTime = 0
        self.endTime = 0
        self.currentTime = self.startTime

        self.numberOfProcess = 10
        self.record = []

        self.meanInterIOInterval = (30,35,40,45,50,55,60,65,70,75)
        self.IOTime = 60
        self.emptyIOQueueTime = 0
        print("start")
        # Create 10 jobs with random execution time uniformly distributed between 120s - 240s
        self.processQ = []
        for i in range(self.numberOfProcess):
            self.processQ.append(Process(i, numpy.random.uniform(120*1000, 240*1000), self.meanInterIOInterval[i]))

        #self.i = 0
        #while(self.i<500):
            #self.i+=1
        while(len(self.processQ) != 0):

            # import process in ready queue
            empty = True
            for process in self.processQ:
                if(process.nextStartTime <= self.currentTime):
                    process.place = "ready queue"
                    print("porocess", process.id, "is in:", process.place)
                    empty = False

            # if ready queue is empty, let time pass to the nextStartTime of next process
            if(empty):
                print("processQ is empty")
                self.processQ = sort("nextStartTime", self.processQ)
                self.currentTime = self.processQ[0].nextStartTime
                self.endTime = self.currentTime
                continue

            # now we have at least one process in ready queue

            # FCFS
            self.processQ = sort("nextStartTime", self.processQ)

            # get next process in ready queue
            p = None
            for i in range(len(self.processQ)):
                p = self.processQ[i]
                if p.place == "ready queue":
                    print("pop", p.id)
                    self.processQ.pop(i)
                    break
                p = None

            # now CPU starts running the process which is stored in p
            p.waitingTime = p.waitingTime + self.currentTime - p.nextStartTime
            if p.id == 0:
                print("waitingTime += self.currentTime - p.nextStartTime", self.currentTime, "-", p.nextStartTime)
            interIOTime = int(numpy.random.exponential(p.meanInterIOInterval)) # lambda= 1/mean
            p.thisRunningTime = int(min(interIOTime, p.leftBurstTime))
            if p.id == 0:
                print("thisRunningTime = min(interIOTime, p.leftBurstTime)", interIOTime, p.leftBurstTime)

            p.leftBurstTime = p.leftBurstTime - p.thisRunningTime
            if p.id == 0:
                print("leftBurstTime is:", p.leftBurstTime)
            p.lastEndTime = self.currentTime + p.thisRunningTime
            p.turnaroundTime = p.lastEndTime - self.startTime
            p.runningTime = p.runningTime + p.thisRunningTime

            if(p.leftBurstTime <=0):# p is finished
                print("process", id, "is finished")
                self.record.append([p.turnaroundTime, p.runningTime, p.waitingTime])

            else: # p is not finished and p is in I/O queue
                p.nextStartTime = int(max(p.lastEndTime, self.emptyIOQueueTime) + self.IOTime)
                p.place = "I/O queue"
                self.emptyIOQueueTime = p.nextStartTime
                self.processQ.append(p)

            self.currentTime = p.lastEndTime
            self.endTime = self.currentTime

        ################################ print result ################################
        sumTurnaroundTime = 0
        sumRunningTime = 0
        sumWaitingTime = 0
        for info in self.record:
            sumTurnaroundTime += info[0]
            sumRunningTime += info[1]
            sumWaitingTime += info[2]

        CPUUtilization = round(float(sumRunningTime)/(float(self.endTime)-float(self.startTime))*100, 2) # %
        throughput = round(float(self.numberOfProcess) / (float(self.endTime)-self.startTime)/float(1000)/float(60), 2) # process per minute
        averageTurnaroundTime = round(float(sumTurnaroundTime)/1000/60/self.numberOfProcess, 2) # mimute per process
        averageWaitingTime = round(float(sumWaitingTime)/1000/60/self.numberOfProcess, 2) # minutes per process

        print("CPU utilization:",CPUUtilization,"%")
        print("Throughput:",throughput,"processes/minute")
        print("Average turnaround time:",averageTurnaroundTime,"minutes/process")
        print("Average waiting time:",averageWaitingTime,"minutes/process")

        # print result in FCFS_output.txt
        self.file.write("CPU utilization:"+str(CPUUtilization)+"%")
        self.file.write("Throughput:"+str(throughput)+"processes/minute")
        self.file.write("Average turnaround time:"+str(averageTurnaroundTime)+"minutes/process")
        self.file.write("Average waiting time:"+str(averageWaitingTime)+"minutes/process")


if __name__ == "__main__":
    FCFS()