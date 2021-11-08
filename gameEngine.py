#coding:utf-8

"""
author : Gerald Pellegrino
date of creation : 02/10/2021
"""
import tkinter as tk
from PIL import Image, ImageTk


class Window:
    def __init__(self, size: str, name: str, bg: str=None):
        self.WINDOW_NAME = name
        #get window height and width
        a = size.index("x")
        self.WINDOW_WIDTH = int(size[:a])
        self.WINDOW_HEIGHT = int(size[a+1:])

        self.window = tk.Tk()
        self.window.geometry(size)
        self.window.title(name)
        self.window.config(bg=bg)
    
    def addBackgroundImage(
                self, image_link: str, 
                bheight: int ="DEFAULT", 
                bwidth: int="DEFAULT", 
                side=tk.LEFT
        ):
        
        self.backgroundCanv = tk.Canvas(self.window, height=self.WINDOW_HEIGHT if bheight == "DEFAULT" else bheight,
                                                     width=self.WINDOW_WIDTH if bwidth == "DEFAULT" else bwidth,
                                                     highlightthickness=0)
        self.backgroundCanv.pack(side=side, padx=None, pady=None)
        img = Image.open(image_link)
        img = img.resize((bwidth if bwidth != "DEFAULT" else self.WINDOW_WIDTH, bheight if bheight != "DEFAULT" else self.WINDOW_HEIGHT), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.backgroundCanv.create_image(0, 0, anchor="nw", image=self.image)

    def openSelectionWindow(self):
        pass
    
    
class Character:

    def __init__(self, container: tk.Canvas, name: str, img_link: str, coordinates: tuple, bwidth, bheight, tag):
        self.name = name
        self.coordinates = coordinates
        self.container = container

        img = Image.open(img_link)
        img = img.resize((bwidth, bheight), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        container.create_image(coordinates[0], coordinates[1], anchor="nw", image=self.image, tag=tag)
    
    def move(self, coordinates):
        deplacement_X = coordinates[0] - self.coordinates[0]
        deplacement_Y = coordinates[1] - self.coordinates[1]
        tag = self.container.gettags(self.tag)[0]
        self.container.move(tag, deplacement_X, deplacement_Y)
        self.clicked = False
        self.coordinates = coordinates

def setimage(img_link, bwidth, bheight):
    img = Image.open(img_link)
    img = img.resize((bwidth, bheight), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)
        
    
if __name__ == "__main__":
    window = Window("800x504", "testing")

    window.addBackgroundImage("graphics/chess_board_brown.png", bwidth=504)

    window.window.mainloop()
