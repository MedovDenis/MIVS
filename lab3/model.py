from colorama import Fore, Style
from pandas import DataFrame
import plotly.express as px
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

logs = {
    "signal" : [],
    "event" : [], 
    "time_event" : [],
    "next_event" : [], 
    "time_next_event" : []
}

time = 1
while queue and (TIME_LIMIT > time):
    for sign in filter(lambda sign: sign[1] <= time, queue):
        queue.remove(sign)
        time_sleep = time_deactivate_event(time)
        sleep[sign[0]] = time_sleep

        logs["signal"].append("said")
        logs["event"].append(events[sign[0]])
        logs["time_event"].append(time)
        logs["next_event"].append("deactivate")
        logs["time_next_event"].append(time_sleep)

        print(Fore.GREEN, "Said:", Fore.WHITE, events[sign[0]], "Time:", time, "Time deactivate:", time_sleep)

    for dp in filter(lambda dp: sleep[dp] == time, sleep):
        time_event = time_activate_event(time)
        queue.append((dp, time_event))

        logs["signal"].append("waid")
        logs["event"].append(events[dp])
        logs["time_event"].append(time)
        logs["next_event"].append("activate")
        logs["time_next_event"].append(time_event)

        print(Fore.YELLOW, "Wait:", Fore.WHITE, events[dp], "Time:", time, "Time activate:  ", time_event)
    time += 1

print(Style.RESET_ALL)

df = DataFrame(logs)
fig = px.scatter(df, y="event", x="time_event", color="signal")
fig.show()
