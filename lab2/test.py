import numpy as np

def generate_information_flow(N :int, alfa: float, beta: float, q: float, t: int):
        
    flow = (beta - alfa) * np.random.sample(N) + alfa + q
    
    summ = 0
    intervals = []
    sub_interval = []

    for x in flow:
        summ += x
        if summ <= t:
            sub_interval.append(x)
        else:
            intervals.append(sub_interval)
            sub_interval = []
            summ = 0

    intervals.append(sub_interval)

    summ_mass = [sum(j) for j in intervals]
    count_mass = [len(j) for j in intervals]
    
    print(intervals)
    print(len(intervals))
    print(summ_mass)
    print(count_mass)


generate_information_flow(1000, 0.50, 1.50, 11.50, 300)