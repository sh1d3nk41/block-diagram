from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from tkinter import Tk, Canvas, Frame, BOTH, Button, Label, Entry
from tkinter import *

app = FastAPI()

class Example(Frame):

    dict_size = {}
    dict_x = {}
    dict_y = {}

    def __init__(self):
        super().__init__()
        self.initUI()


    def Build (self, value):
        x = self.dict_x[value]
        y = self.dict_y[value]
        self.canvas.create_rectangle(x, y, x+200, y+75, width=1)
        self.canvas.create_text(((x + x + 200) / 2), ((y + y+75) / 2), text=value, font=("Kontemporary", 20))

    def Size(self, prev_value, next_value):
        if (self.dict_size[prev_value] < 3) or (prev_value in self.dict_size):
            self.dict_size[next_value] = 0
            if (self.dict_size[prev_value] == 0):
                self.dict_x[next_value] = self.dict_x.get(prev_value)
                self.dict_y[next_value] = self.dict_y.get(prev_value) + 100
                self.canvas.create_line((self.dict_x.get(prev_value)+200/2), self.dict_y.get(prev_value)+75,
                                        (self.dict_x.get(prev_value)+200/2), self.dict_y.get(prev_value)+100)
            elif (self.dict_size[prev_value] == 1):
                self.dict_x[next_value] = self.dict_x.get(prev_value) - 250
                self.dict_y[next_value] = self.dict_y.get(prev_value)
                self.canvas.create_line((self.dict_x.get(prev_value), (self.dict_y.get(prev_value) + 75/2),
                                        (self.dict_x.get(prev_value) - 50), (self.dict_y.get(prev_value) + 75/2)))
            elif (self.dict_size[prev_value] == 2):
                self.dict_x[next_value] = self.dict_x.get(prev_value) + 250
                self.dict_y[next_value] = self.dict_y.get(prev_value)
                self.canvas.create_line((self.dict_x.get(prev_value) + 200, (self.dict_y.get(prev_value) + 75 / 2),
                                         (self.dict_x.get(prev_value) + 250), (self.dict_y.get(prev_value) + 75 / 2)))
            self.Build(next_value)
            self.dict_size[prev_value] += 1


    def initUI(self):
        self.master.title("Test")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)  # Store the canvas as an instance variable

        btn_exit = Button(text="Create", font=("Kontemporary", 30), activebackground="#fa0202", fg="#bd2626",
                          command=lambda: self.Size(enter_prev.get(), enter_next.get()))
        self.canvas.create_window(40, 250, anchor=NW, window=btn_exit, width=200, height=50)

        prev_text = Label(text="Enter the previous graph", font=("Kontemporary", 30))
        self.canvas.create_window(180, 50, window=prev_text)

        enter_prev = Entry(width=20, font=("Kontemporary", 20))
        self.canvas.create_window(135, 100, window=enter_prev)

        next_text = Label(text="Enter the next graph", font=("Kontemporary", 30))
        self.canvas.create_window(160, 150, window=next_text)

        enter_next = Entry(width=20, font=("Kontemporary", 20))
        self.canvas.create_window(135, 200, window=enter_next)

        self.canvas.pack(fill=BOTH, expand=1)

        self.canvas.create_oval(650, 75, 850, 150, width=1)
        self.canvas.create_text(((650+850)/2), ((150+75)/2), text="Start", font=("Kontemporary", 20))

        self.dict_size["start"]= 0
        self.dict_x["start"]= 650
        self.dict_y["start"] = 75


class Graph(BaseModel):
    prev_value: str
    next_value: str

ex = Example()

@app.post("/add_graph/")
async def add_graph(graph: Graph):
    ex.Size(graph.prev_value, graph.next_value)
    return {"message": "Граф добавлен успешно"}

def run_gui():
    root = Tk()
    root.geometry("1440x900")
    root.mainloop()

if __name__ == '__main__':
    run_gui()
