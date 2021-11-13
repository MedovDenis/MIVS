import random
import json

with open("img/food/food.json", "r") as fl:
    food = json.load(fl)

class Order:
    def __init__(self, number_order):
        self.number_order = number_order
        self.order = random.choice(list(food))
        self.img = "img/food/" + food[self.order]["img"]
        self.time_cooking = None
        
    def init_cooking(self, time):
        self.time_cooking = time + random.randint(food[self.order]["min_time"] , food[self.order]["max_time"])

    def check_cooking(self, time):
        return self.time_cooking <= time

    def info_order(self):
        return food[self.order]
