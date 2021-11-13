from transitions import Machine
from tkinter import * 
from PIL import Image, ImageTk

import time
import threading

import visitor
import cook
import order

TIME_LIMIT = 500

states_visitor = ['order', 'wait', 'eat']
states_cook = ['wait', 'cook']

transitions_visitor = [
    { 'trigger': 'set_order', 'source': 'order', 'dest': 'wait' },
    { 'trigger': 'get_order', 'source': 'wait', 'dest': 'eat' },
    { 'trigger': 'eat_up', 'source': 'eat', 'dest': 'order' }]

transitions_cook = [
    { 'trigger': 'get_order', 'source': 'wait', 'dest': 'cook' },
    { 'trigger': 'set_order', 'source': 'cook', 'dest': 'wait' }]

def thread_modeling():

    time_model = 0
    num_order = 0
    order_ready = None

    lbxLogs.delete(0, END)

    visitors = [
        visitor.Visitor(cvMan1),
        visitor.Visitor(cvMan2),
        visitor.Visitor(cvMan3)]

    for vistr in visitors:
        Machine(vistr, states=states_visitor, transitions=transitions_visitor, initial='order')
        vistr.init_order(time_model, num_order)
        num_order += 1

    chef = cook.Cook(cvKitchen)
    Machine(chef, states=states_cook, transitions=transitions_cook, initial='wait')
    
    while len(list(filter(lambda vistr: vistr.state == "eat", visitors))) < 3 and TIME_LIMIT > time_model:
        for vistr in visitors:
            if vistr.state == "order":
                ordr = vistr.issue_order(time_model)
                if ordr != None:
                    vistr.set_order()
                    logs = "[{}] {} сделал(а) Заказ №{} : {}".format(time_model, vistr.visitor, ordr.number_order, ordr.order)
                    lbxLogs.insert(0, logs)
                    chef.add_order(ordr)

            if vistr.state == "wait":
                if vistr.check_order(order_ready):
                    vistr.init_eat(time_model)
                    vistr.get_order()
                    logs = "[{}] {} получил(а) Заказ №{} : {}".format(time_model, vistr.visitor, vistr.order.number_order, vistr.order.order)
                    lbxLogs.insert(0, logs)

            if vistr.state == "eat":
                if vistr.issue_eat(time_model):
                    vistr.init_order(time_model, num_order)
                    logs = "[{}] {} делает Заказ №{}".format(time_model, vistr.visitor, num_order)
                    lbxLogs.insert(0, logs)
                    num_order += 1
                    vistr.eat_up()
                    
        if chef.state == "wait":
            if chef.queue:
                chef.get_order()
                chef.cook_order(time_model)
                logs = "[{}] Повар готовит Заказ №{} : {}".format(time_model, chef.cook.number_order, chef.cook.order)
                lbxLogs.insert(0, logs)

        if chef.state == "cook":
            order_ready = chef.issue_order(time_model)
            if order_ready != None: 
                chef.set_order()
                logs = "[{}] Повар приготовил Заказ №{} : {}".format(time_model, order_ready.number_order, order_ready.order)
                lbxLogs.insert(0, logs)

        time.sleep(0.1)
        lbTimer["text"] = "Время: {}".format(time_model)
        time_model += 1

    print("end")

def modeling():
    thread = threading.Thread(target=thread_modeling)
    thread.start()

form = Tk()
form.title("Ресторан")

image = Image.open("img/table.png")
table = ImageTk.PhotoImage(image)

image = Image.open("img/oven.png")
kitchen = ImageTk.PhotoImage(image)

lbTimer = Label(form, text="Врeмя:")

cvMan1 = Canvas(form, height=64, width=64)
cvMan2 = Canvas(form, height=64, width=64)
cvMan3 = Canvas(form, height=64, width=64)
cvKitchen = Canvas(form, height=64, width=64)

lbTable1 = Label(form, image=table, height=64)
lbTable2 = Label(form, image=table, height=64)
lbTable3 = Label(form, image=table, height=64)
lbKitchen = Label(form, image=kitchen, height=64)

btnStart = Button(form, text="Start", command=modeling)

lbxLogs = Listbox(form,width=50)

lbTimer.grid(columnspan=4, column=0, row=0)
lbxLogs.grid(rowspan=4, column=4, row=0)

cvMan1.grid(column=0, row=1)
cvMan2.grid(column=1, row=1)
cvMan3.grid(column=2, row=1)
cvKitchen.grid(column=3, row=1)

lbTable1.grid(column=0, row=2)
lbTable2.grid(column=1, row=2)
lbTable3.grid(column=2, row=2)
lbKitchen.grid(column=3, row=2)

btnStart.grid(columnspan=4, column=0, row=3)

form.mainloop()