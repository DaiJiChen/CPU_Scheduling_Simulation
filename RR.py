# Jichen Dai
# I pledge my honor that I have abided by the Stevens Honor System
# This structure of this program referenced https://github.com/qiyunlu/SIT.CS520.theSimulationProgrammingProject
from process import Process
from sort import sort
import numpy
import random

# time unit : ms
class RR:
    def __init__(self):
        self.file = open("RR_output.txt", 'a')
        self.startTime = 0
        self.endTime = 0
        self.currentTime = self.startTime

        self.numberOfProcess = 10
        self.record = []  # record[p] = [p.turnaroundTime, p.runningTime, p.waitingTime]

        self.meanInterIOInterval = (30,35,40,45,50,55,60,65,70,75)
        self.IOTime = 60
        self.emptyIOQueueTime = 0

        self.orderL = []

        self.quantum = 50



        # Create 10 jobs with random execution time uniformly distributed between 120s - 240s
        self.processQ = []
        for i in range(self.numberOfProcess):
            # the randomness of the execution time of a process is mitigated to vary from 150 to 210
            self.processQ.append(Process(i, 120+int(random.uniform(30, 90)), self.meanInterIOInterval[i]))

        self.i = 0
        while(len(self.processQ) != 0 ):
            self.i += 1

            # import process in ready queue
            empty = True
            for process in self.processQ:
                if(process.nextReadyTime <= self.currentTime):
                    process.place = "ready queue"
                    empty = False

            # if ready queue is empty, let time pass to the nextReadyTime of next process
            if(empty):
                self.processQ = sort("nextReadyTime", self.processQ)
                self.currentTime = self.processQ[0].nextReadyTime
                self.endTime = self.currentTime
                continue
            # now we have at least one process in ready queue


            # RR
            self.processQ = sort("nextReadyTime", self.processQ)

            # get next process in ready queue
            p = None
            for i in range(len(self.processQ)):
                p = self.processQ[i]
                if p.place == "ready queue":
                    self.processQ.pop(i)
                    break
                p = None





            ########################## now CPU starts running the process which is stored in p #########################
            clockInterrupt = False
            p.waitingTime = p.waitingTime + self.currentTime - p.nextReadyTime
            # in order to mitigate the randomness, the weight of the exponential random value is set to 0.3
            interIOTime = int(0.7*p.meanInterIOInterval + 0.3*numpy.random.exponential(p.meanInterIOInterval)) # lambda= 1/mean
            p.thisRunningTime = int(min(interIOTime, p.leftBurstTime))
            if(p.thisRunningTime >= self.quantum):
                p.thisRunningTime = self.quantum
                clockInterrupt = True

            p.leftBurstTime = p.leftBurstTime - p.thisRunningTime
            p.lastEndTime = self.currentTime + p.thisRunningTime
            p.turnaroundTime = p.lastEndTime - self.startTime
            p.runningTime = p.runningTime + p.thisRunningTime


            if p.leftBurstTime <=0 :# p is finished
                self.record.append([p.turnaroundTime, p.runningTime, p.waitingTime])

            elif clockInterrupt: # p is not finished and is interupted by clock
                p.nextReadyTime = p.lastEndTime
                p.place = "ready queue"
                self.processQ.append(p)

            else: # p is not finished and p is in I/O queue
                p.nextReadyTime = int(max(p.lastEndTime, self.emptyIOQueueTime) + self.IOTime)
                p.place = "I/O queue"
                self.emptyIOQueueTime = p.nextReadyTime
                self.processQ.append(p)

            self.orderL.append(p.id)
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
        throughput = round(float(self.numberOfProcess) / ((float(self.endTime)-self.startTime)/1000/60), 2) # process per minute
        averageTurnaroundTime = round(float(sumTurnaroundTime)/1000/60/self.numberOfProcess, 2) # mimute per process
        averageWaitingTime = round(float(sumWaitingTime)/1000/60/self.numberOfProcess, 5) # minutes per process

        print("CPU utilization:",CPUUtilization,"%")
        print("Throughput:",throughput,"processes/minute")
        print("Average turnaround time:",averageTurnaroundTime,"minutes/process")
        print("Average waiting time:",averageWaitingTime,"minutes/process")
        print('\n                        -------------------------Gantt Chart   (RR  quantum =' + str(self.quantum) + '  Time unit is: ms)-------------------------')
        string = ""
        for i in range(len(self.orderL)):
            string = string + "|P" + str(self.orderL[i])
        print(string)

        # print result in FCFS_output.txt
        self.file.write("\nCPU utilization:"+str(CPUUtilization)+"%")
        self.file.write("\nThroughput:"+str(throughput)+"processes/minute")
        self.file.write("\nAverage turnaround time:"+str(averageTurnaroundTime)+"minutes/process")
        self.file.write("\nAverage waiting time:"+str(averageWaitingTime)+"minutes/process")
        self.file.write('\n                        -------------------------Gantt Chart   (RR  quantum =' + str(
            self.quantum) + '  Time unit is: ms)-------------------------\n')
        self.file.write(string)



if __name__ == "__main__":
        RR()