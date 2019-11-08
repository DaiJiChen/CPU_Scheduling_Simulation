import numpy

if __name__ == "__main__":
    sum = 0
    for i in range(1000):
        sum += numpy.random.uniform(120, 240)
    average = sum/1000
    print(average)
    print(max(1,2))