from colorama import Fore, Style
import numpy as np
import json

TIME_LIMIT = 10000

with open('events.json', 'r', encoding='utf-8') as fh:
    events = json.load(fh)

def time_activate_event(time = 0):
    return time + np.random.randint(10, 40)

def time_deactivate_event(time = 0):
    return time + np.random.randint(5, 10)

queue = [(event,  time_activate_event()) for event in events]
sleep = dict((event, 0) for event in events)

time = 1
while queue and (TIME_LIMIT > time):
    for sign in filter(lambda sign: sign[1] <= time, queue):
        queue.remove(sign)
        time_sleep = time_deactivate_event(time)
        sleep[sign[0]] = time_sleep
        print(Fore.GREEN, "Said:", Fore.WHITE, events[sign[0]], "Time:", time, "Time deactivation:", time_sleep)

    for dp in filter(lambda dp: sleep[dp] == time, sleep):
        time_event = time_activate_event(time)
        queue.append((dp, time_event))
        print(Fore.YELLOW, "Waid:", Fore.WHITE, events[dp], "Time:", time, "Time activation:", time_event)
    time += 1

print(Style.RESET_ALL)





