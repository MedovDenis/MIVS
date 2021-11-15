from tkinter import Canvas
from PIL import Image, ImageTk

import random
import json

from order import Order

with open("img/people/people.json", "r") as fl:
    people = json.load(fl)

class Visitor:
    def __init__(self, cvPeople:Canvas, cvStatus:Canvas):
        self.visitor = random.choice(list(people))

        self.img = ImageTk.PhotoImage(Image.open("img/people/" + people[self.visitor]["img"]))
        self.paper = ImageTk.PhotoImage(Image.open("img/menu.png"))
        self.timer = ImageTk.PhotoImage(Image.open("img/timer.png"))

        self.size = self.img.width()

        self.cvPeople = cvPeople
        self.cvPeople.delete("all")
        self._print_image(self.cvPeople, self.img)

        self.cvStatus = cvStatus

        self.time_order = None
        self.time_eat = None
        self.order = None

    def init_order(self, time, num_order):
        self.cvStatus.delete("all")
        self._print_image(self.cvStatus, self.paper)
        self.time_order = time + random.randint(people[self.visitor]["min_time_order"], people[self.visitor]["max_time_order"])
        self.order = Order(num_order)

    def issue_order(self, time):
        if self.time_order == time:
            self.cvStatus.delete("all")
            self._print_image(self.cvStatus, self.timer)
            return self.order
        return None

    def check_order(self, order):
        return self.order == order
    
    def init_eat(self, time):
        img = ImageTk.PhotoImage(Image.open(self.order.img))
        self.cvStatus.delete("all")
        self._print_image(self.cvStatus, img)
        self.time_eat = time + random.randint(people[self.visitor]["min_time_eat"], people[self.visitor]["max_time_eat"])

    def issue_eat(self, time:int):
        if self.time_eat != None:
            return self.time_eat <= time

    def _print_image(self, cavans:Canvas, image:ImageTk.PhotoImage):
        cavans.create_image(self.size/2,self.size/2,image=image)
        cavans.image = image

    def visitor_info(self):
        return people[self.visitor]