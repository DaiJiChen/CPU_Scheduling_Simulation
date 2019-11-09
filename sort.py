# scheduling processes in queue ( Increasing order )
def sort(key, Q):
    processQ = Q
    # scheduling by burst time
    if(key == "predictburstTime"):
        for i in range(len(processQ)-1):
            flag = 0
            for j in range(len(processQ)-1):
                if(processQ[j].predictBurstTime>processQ[j+1].predictBurstTime):
                    processQ[j], processQ[j+1] = processQ[j+1], processQ[j]
                    flag = 1
            if flag == 0:
                break

    # scheduling by arrival time
    if (key == "nextReadyTime"):
        for i in range(len(processQ)-1):
            flag = 0
            for j in range(len(processQ)-1):
                if (processQ[j].nextReadyTime > processQ[j + 1].nextReadyTime):
                    processQ[j], processQ[j + 1] = processQ[j + 1], processQ[j]
                    flag = 1
            if flag == 0:
                break

    # scheduling by priority
    if (key == "priority"):
        for i in range(len(processQ)-1):
            flag = 0
            for j in range(len(processQ)-1):
                if (processQ[j].priority > processQ[j + 1].priority):
                    processQ[j], processQ[j + 1] = processQ[j + 1], processQ[j]
                    flag = 1
            if flag == 0:
                break
    return Q