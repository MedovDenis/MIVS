from tkinter import Canvas
from PIL import Image, ImageTk

import order 

class Cook:
    def __init__(self, canvas:Canvas):
        self.queue = []
        self.cook = None

        self.canvas = canvas
        image = Image.open("img/chef.png")
        self.canvas.delete("all")
        self.chef = ImageTk.PhotoImage(image)
        self._print_image(self.chef)
        
    def add_order(self, order:order.Order):
        self.queue.insert(0, order)

    def cook_order(self, time:int):
        self.cook = self.queue.pop()
        img = ImageTk.PhotoImage(Image.open(self.cook.img))
        self._print_image(img)
        self.cook.init_cooking(time)

    def issue_order(self, time:int):
        if self.cook.check_cooking(time):
            self.canvas.delete("all")
            self._print_image(self.chef)
            cook = self.cook 
            self.cook = None
            return cook   
        return None

    def _print_image(self, image):
        self.canvas.create_image(32,32,image=image)
        self.canvas.image = image
