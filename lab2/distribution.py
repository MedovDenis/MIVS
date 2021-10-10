import numpy as np

def generate_information_flow(N :int, alfa: float, beta: float, q: float, t: int):
        
    flow = (beta - alfa) * np.random.sample(N) + alfa + q
    
    summ = 0
    intervals = []
    sub_interval = []
    time_interval = []
    time = 0
    for x in flow:
        summ += round(x, 2)
        if summ <= t:
            sub_interval.append(round(x, 2))
        else:
            time_interval.append({"start" : time, "end" : time + t})
            time += t
            intervals.append(sub_interval)
            sub_interval = [round(x, 2)]
            summ = round(x, 2)

    # intervals.append(sub_interval)

    summ_applications = [round(sum(j), 2) for j in intervals]
    number_applications = [round(len(j), 2) for j in intervals]
    average_time_flow = [round(sum(j) / len(j), 2) for j in intervals]

    table_header = ['№', 'Начало интервала', 'Конец интервала', 'Кол-во заявок', 'Ср. время заявки', 'Общее время заявок']
    table_items = [[i + 1, time_interval[i]['start'], time_interval[i]['end'], number_applications[i], average_time_flow[i], summ_applications[i]] for i in range(len(intervals))]

    info = {
        'Кол-во потоков' : len(intervals),
        'Общее время' : round(sum(summ_applications), 2),
        'Cр. время заявки': round((sum(average_time_flow) / len(average_time_flow)), 2),
        'Ср. кол-во заявок': round(sum(number_applications) / len(number_applications), 2),
        'Ср. время потока': round(sum(summ_applications) / len(summ_applications), 2)
    }

    times = [item['end'] - t / 2 for item in time_interval]
    width = [item['end'] - item['start'] for item in time_interval]

    graph = {
        'data': [
            {'x': times, 'y': number_applications, 'type': 'bar', 'width': width}
        ], 
        'layout': {'title': 'Гистограмма'}
    }

    return{
        'graph' : graph,
        'info' : info,
        'table_header' : table_header,
        'table_items' : table_items
    } 
        