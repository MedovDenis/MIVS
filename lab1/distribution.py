import numpy as np

def generate_distribution (N, a, n, alfa):
    r = np.random.sample(N)
    x = np.sort([a * np.sqrt(1 - (1 - i)**2) for i in r])

    min, max = np.min(x), np.max(x)

    # n = int(np.log2(N)) + 1

    # step = a / n

    p = [min]
    p_next = np.sqrt(a**2 - (np.sqrt(a**2 - min**2) - a/n)**2)

    while(p_next < max):
        p.append(p_next)
        p_next = np.sqrt(a**2 - (np.sqrt(a**2 - p_next**2) - a/n)**2)
        if (len(p) >= n): break
    p.append(a)

    # p = [i*step for i in range(n + 1)]

    intervals = [{'pf': p[i], 'pe': p[i + 1]} for i in range(n)]

    counters = []
    for interval in intervals:
        count = 0
        for item in x:
            if item >= interval['pf'] and item < interval['pe']:
                count += 1
        counters.append(count)

    pc = [ interval['pe'] - (interval['pe'] - interval['pf']) / 2 for  interval in intervals ]

    width = [ interval['pe'] - interval['pf'] for interval in intervals ]

    height = [ (counters[i] / N) / width[i] for i in range(n)]

    # chisquare = np.sum([((counters[i] - N*p[i+1])**2)/(N*p[i+1]) for i in range(n)])
    chisquare = np.sum([(counters[i]**2) for i in range(n)]) * (n/N) - N

    graph = {
        'data': [
            {'x' : pc, 'y' : height}, 
            {'x': pc, 'y': height, 'type': 'bar', 'width': width}
        ], 
        'layout': {'title': 'Гистограмма'}
    }

    info = {
        'N': N,
        'a': a,
        'n': n,
        'alfa': alfa,
        'min': round(min, 5),
        'max': round(max, 5),
        'chisquare': round(chisquare, 5)
    }

    table_header = ['№','Начало интервала', 'Конец интервала', 'Кол-во', 'Ширина', 'Высота', 'Частота']
    table_items = [[
        i + 1, 
        round(intervals[i]['pf'], 5), 
        round(intervals[i]['pe'], 5), 
        counters[i], 
        round(width[i], 5), 
        round(height[i], 5),
        round(counters[i] / N, 5)
        ] for i in range(n)
    ]

    return {
        'graph': graph,
        'info': info,
        'table_header': table_header,
        'table_items': table_items
    }