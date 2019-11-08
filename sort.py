# scheduling processes in queue ( Increasing order )
def sort(key, Q):
    processQ = Q
    # scheduling by burst time
    if(key == "burstTime"):
        for i in range(len(processQ)):
            flag = 0
            for j in range(len(processQ)-1):
                if(processQ[j].burstTime>processQ[j+1].burstTime):
                    processQ[j], processQ[j+1] = processQ[j+1], processQ[j]
                    flag = 1
            if flag == 0:
                break

    # scheduling by arrival time
    if (key == "nextStartTime"):
        for i in range(len(processQ)):
            flag = 0
            for j in range(len(processQ)-1):
                if (processQ[j].nextStartTime > processQ[j + 1].nextStartTime):
                    processQ[j], processQ[j + 1] = processQ[j + 1], processQ[j]
                    flag = 1
            if flag == 0:
                break

    # scheduling by priority
    if (key == "priority"):
        for i in range(len(processQ)):
            flag = 0
            for j in range(len(processQ)-1):
                if (processQ[j].priority > processQ[j + 1].priority):
                    processQ[j], processQ[j + 1] = processQ[j + 1], processQ[j]
                    flag = 1
            if flag == 0:
                break
    return Q