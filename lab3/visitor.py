from tkinter import Canvas
from PIL import Image, ImageTk

import random
import json

from order import Order

with open("img/people/people.json", "r") as fl:
    people = json.load(fl)

class Visitor:
    def __init__(self, canvas:Canvas):
        self.visitor = random.choice(list(people))

        self.canvas = canvas
        self.canvas.delete("all")
        self.img = ImageTk.PhotoImage(Image.open("img/people/" + people[self.visitor]["img"]))
        self.paper = ImageTk.PhotoImage(Image.open("img/menu.png"))
        self._print_image(self.img)

        self.time_order = None
        self.time_eat = None
        self.order = None

    def init_order(self, time, num_order):
        self._print_image(self.paper)
        self.time_order = time + random.randint(people[self.visitor]["min_time_order"], people[self.visitor]["max_time_order"])
        self.order = Order(num_order)

    def issue_order(self, time):
        if self.time_order == time:
            self.canvas.delete("all")
            self._print_image(self.img)
            return self.order
        return None

    def check_order(self, order):
        return self.order == order
    
    def init_eat(self, time):
        img = ImageTk.PhotoImage(Image.open(self.order.img))
        self.canvas.delete("all")
        self._print_image(self.img)
        self._print_image(img)
        self.time_eat = time + random.randint(people[self.visitor]["min_time_eat"], people[self.visitor]["max_time_eat"])

    def issue_eat(self, time:int):
        if self.time_eat != None:
            return self.time_eat <= time

    def _print_image(self, image):
        self.canvas.create_image(32,32,image=image)
        self.canvas.image = image

    def visitor_info(self):
        return people[self.visitor]