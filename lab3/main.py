from tkinter import * 
from PIL import Image, ImageTk
from pandas import DataFrame
import plotly.express as px
import numpy as np
import time
import threading

TIME_LIMIT = 10000
events = {
        "p1" : "Событие 1",
        "p2" : "Событие 2",
        "p3" : "Событие 3"
    }

def time_activate_event(time = 0):
    return time + np.random.randint(10, 40)

def time_deactivate_event(time = 0):
    return time + np.random.randint(5, 10)


def thread_modeling():

    image = Image.open("img/man/man1.png")
    man1 = ImageTk.PhotoImage(image)

    image = Image.open("img/man/man2.png")
    man2 = ImageTk.PhotoImage(image)

    image = Image.open("img/man/man3.png")
    man3 = ImageTk.PhotoImage(image)

    queue = [(event,  time_activate_event()) for event in events]
    sleep = dict((event, 0) for event in events)

    logs = {
        "signal" : [],
        "event" : [], 
        "time_event" : [],
        "next_event" : [], 
        "time_next_event" : []
    }

    lbxLogs.delete(0, END)
    cvMan1.create_image(32,32,image = man1)
    cvMan2.create_image(32,32,image = man2)
    cvMan3.create_image(32,32,image = man3)

    time_model = 1
    while queue and (TIME_LIMIT > time_model):
        lbTimer["text"] = "Время: {}".format(time_model)

        for sign in filter(lambda sign: sign[1] <= time_model, queue):
            queue.remove(sign)
            time_sleep = time_deactivate_event(time_model)
            sleep[sign[0]] = time_sleep

            logs["signal"].append("said")
            logs["event"].append(events[sign[0]])
            logs["time_event"].append(time_model)
            logs["next_event"].append("deactivate")
            logs["time_next_event"].append(time_sleep)
            lbxLogs.insert(0, "Said: {}, Time: {}".format(events[sign[0]], time_model))
            print(sign[0])
            if (sign[0] == "p1"):
                print(1)
                cvMan1.delete("all")
            if (sign[0] == "p2"):
                cvMan2.delete("all")
            if (sign[0] == "p3"):
                cvMan3.delete("all")
            # print("Said:", events[sign[0]], "Time:", time_model, "Time deactivate:", time_sleep)

        for dp in filter(lambda dp: sleep[dp] == time_model, sleep):
            time_event = time_activate_event(time_model)
            queue.append((dp, time_event))

            logs["signal"].append("waid")
            logs["event"].append(events[dp])
            logs["time_event"].append(time_model)
            logs["next_event"].append("activate")
            logs["time_next_event"].append(time_event)
            lbxLogs.insert(0, "Wait: {}, Time: {}".format(events[dp], time_model))
            if (sign[0] == "p1"):
                cvMan1.create_image(32,32,image = man1)
            if (sign[0] == "p2"):
                cvMan2.create_image(32,32,image = man2)
            if (sign[0] == "p3"):
                cvMan3.create_image(32,32,image = man3)

            # print("Wait:", events[dp], "Time:", time_model, "Time activate:  ", time_event)

        time.sleep(0.1)
        time_model += 1

def modeling():
    thread = threading.Thread(target=thread_modeling)
    thread.start()


form = Tk()  
form.title("Ресторан")    

image = Image.open("img/table.png")
table = ImageTk.PhotoImage(image)

lbTimer = Label(form, text="Врмя:")

cvMan1 = Canvas(form, image=None, height=64, width=64)
cvMan2 = Canvas(form, image=None, height=64, width=64)
cvMan3 = Canvas(form, image=None, height=64, width=64)

lbTable1 = Label(form, image=table, height=64)
lbTable2 = Label(form, image=table, height=64)
lbTable3 = Label(form, image=table, height=64)

btnStart = Button(form, text="Start", command=modeling)

lbxLogs = Listbox(form,width=50)

lbTimer.grid(columnspan=3, column=0, row=0)
lbxLogs.grid(rowspan=4, column=3, row=0)

cvMan1.grid(column=0, row=1)
cvMan2.grid(column=1, row=1)
cvMan3.grid(column=2, row=1)

lbTable1.grid(column=0, row=2)
lbTable2.grid(column=1, row=2)
lbTable3.grid(column=2, row=2)

btnStart.grid(columnspan=3, column=0, row=3)


form.mainloop()




