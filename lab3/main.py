from tkinter import font
from transitions import Machine
from tkinter import * 
from PIL import Image, ImageTk

import time
import threading

import visitor
import cook
import order

SIZE = 128
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
        visitor.Visitor(cvMan1, cvState1),
        visitor.Visitor(cvMan2, cvState2),
        visitor.Visitor(cvMan3, cvState3)]

    for vistr in visitors:
        Machine(vistr, states=states_visitor, transitions=transitions_visitor, initial='order')
        vistr.init_order(time_model, num_order)
        num_order += 1

    chef = cook.Cook(cvKitchen, cvState4)
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

        time.sleep(0.2)
        lbTimer["text"] = "Время: {}".format(time_model)
        time_model += 1

    print("end")


def modeling():
    thread = threading.Thread(target=thread_modeling)
    thread.start()


form = Tk()
form.title("Ресторан")
form.config(bg="#65C8F5")

image = Image.open("img/table.png")
table = ImageTk.PhotoImage(image)

image = Image.open("img/oven.png")
kitchen = ImageTk.PhotoImage(image)

lbTimer = Label(form, text="Врeмя:", font=("Helvetica", 18, font.BOLD), bg="#65C8F5")

cvMan1 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvMan2 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvMan3 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvKitchen = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")

cvState1 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvState2 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvState3 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")
cvState4 = Canvas(form, height=SIZE, width=SIZE, bg="#65C8F5")

lbTable1 = Label(form, image=table, height=SIZE, bg="#65C8F5")
lbTable2 = Label(form, image=table, height=SIZE, bg="#65C8F5")
lbTable3 = Label(form, image=table, height=SIZE, bg="#65C8F5")
lbKitchen = Label(form, image=kitchen, height=SIZE, bg="#65C8F5")

btnStart = Button(form, text="Start", command=modeling, font=("Helvetica", 18, font.BOLD), width=10)

lbxLogs = Listbox(form, height=18, width=45, font=("Helvetica", 18, font.BOLD))

lbTimer.grid(columnspan=4, column=0, row=0)
lbxLogs.grid(rowspan=5, column=4, row=0)

cvMan1.grid(column=0, row=1, padx=10)
cvMan2.grid(column=1, row=1, padx=10)
cvMan3.grid(column=2, row=1, padx=10)
cvKitchen.grid(column=3, row=1, padx=30)

cvState1.grid(column=0, row=2)
cvState2.grid(column=1, row=2)
cvState3.grid(column=2, row=2)
cvState4.grid(column=3, row=2)

lbTable1.grid(column=0, row=3)
lbTable2.grid(column=1, row=3)
lbTable3.grid(column=2, row=3)
lbKitchen.grid(column=3, row=3)

btnStart.grid(columnspan=4, column=0, row=4)

form.mainloop()