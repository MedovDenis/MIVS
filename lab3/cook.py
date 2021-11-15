from tkinter import Canvas
from PIL import Image, ImageTk

import order 

class Cook:
    def __init__(self, cvCook:Canvas, cvStatus:Canvas):
        self.queue = []
        self.cook = None

        self.img_chef = ImageTk.PhotoImage(Image.open("img/chef.png"))
        self.img_break = ImageTk.PhotoImage(Image.open("img/break.png"))

        self.cvCook = cvCook
        self.cvStatus = cvStatus
    
        self.size = self.img_chef.width()

        self.cvCook.delete("all")
        self._print_image(self.cvCook, self.img_chef)

        self.cvStatus.delete("all")
        self._print_image(self.cvStatus, self.img_break)
        
    def add_order(self, order:order.Order):
        self.queue.insert(0, order)

    def cook_order(self, time:int):
        self.cook = self.queue.pop()
        img = ImageTk.PhotoImage(Image.open(self.cook.img))
        self.cvStatus.delete("all")
        self._print_image( self.cvStatus, img)
        self.cook.init_cooking(time)

    def issue_order(self, time:int):
        if self.cook.check_cooking(time):
            self.cvStatus.delete("all")
            self._print_image(self.cvStatus, self.img_break)
            cook = self.cook 
            self.cook = None
            return cook   
        return None

    def _print_image(self, cavans:Canvas, image:ImageTk.PhotoImage):
        cavans.create_image(self.size/2,self.size/2, image=image)
        cavans.image = image
