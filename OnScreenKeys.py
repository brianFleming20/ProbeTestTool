"""
Created on 3 May 2017
@author: Brian F
Creates an onscreen keyboard that interacts with a system.
Extra functions to convert letters to upper case.
Copy characters are displayed so that the user can see the letter or number pressed.
The data is recorded to the local cache.
"""
import Datastore
from tkinter import *
from tkinter import Tk
from time import sleep

_TITLE = "This is the title"
PTT_Version = 'self.canvasboard By Danish'  # title Name
GREEN = "#9bdeac"
FONT_NAME = "Courier"
DS = Datastore.DataStore()


# showing all data in display
def convert_key(key):
    if ord(key) > 64:
        upp = key.upper()
    else:
        upp = key
    return upp


def wait_for_response(master, label, block=False, width=110, x=0.7, y=0.25):
    DS.write_to_from_keys("")
    password_blank = "*********************"
    while 1:
        pw_data = DS.get_keyboard_data()
        pw_len = len(pw_data)
        if pw_len > 0 and pw_data[-1] == "+":
            pw_data = pw_data[:-1]
            break
        if block:
            master.itemconfig(label, text=password_blank[:pw_len])
            Label(master, text=password_blank[:pw_len], font=("bold", 15)).place(relx=x, rely=y, width=width,
                                                                                 anchor=N)
        else:
            master.itemconfig(label, text=pw_data)
            Label(master, text=pw_data, font=("bold", 15)).place(relx=x, rely=y, width=width, anchor=N)
        Tk.update(master)
    return pw_data


class Keyboard:
    def __init__(self):
        self.name_text = None
        self.canvas = None
        self.shift_lock = None
        # self.canvas = Canvas(width=1100, height=280)
        self.keys = ""
        self.first_row = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.second_row = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '@']
        self.third_row = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
        self.forth_row = ['z', 'x', 'c', 'v', 'b', 'n', 'm', '/', '?', '.']

    # First Line Button
    def get_keyboard(self):
        self.shift_lock = False
        self.canvas = Canvas(width=1100, height=275)
        self.canvas.place(x=120, y=550)
        # Numbers section
        self.name_text = self.canvas.create_text(70, 18, text="lower case", fill="black", font=(FONT_NAME, 12, "bold"))
        locx1 = 0.06
        locy1 = 0.2
        for key in self.first_row:
            self.display_keys(key, locx1, locy1)
            locx1 += 0.082
        locxc = 0.9
        clear = Button(self.canvas, text='Clear', width=10, font=("Courier", 12), command=self.clear)
        clear.place(relx=locxc, rely=locy1, anchor=CENTER)
        # Frist letter row
        locx2 = 0.08
        locy2 = 0.36
        for key in self.second_row:
            self.display_keys(key, locx2, locy2)
            locx2 += 0.082
        # Second Letter Line
        locx3 = 0.1
        locy3 = 0.52
        for key in self.third_row:
            self.display_keys(key, locx3, locy3)
            locx3 += 0.082
        enter = Button(self.canvas, text='Enter', width=15, font=("Courier", 16, "bold"), background="#68B984",
                       command=lambda check='+': self.end_keyboard(check))
        enter.place(relx=0.9, rely=locy3, anchor=CENTER)
        # third line Button
        locx4 = 0.18
        locy4 = 0.7
        for key in self.forth_row:
            self.display_keys(key, locx4, locy4)
            locx4 += 0.082
        locx5 = 0.09
        shift = Button(self.canvas, text='Shift Lock', width=10, font=('Arial', 12), command=lambda: self.shift())
        shift.place(relx=locx5, rely=locy4, anchor=CENTER)
        # Fourth Line Button
        space_text = " "
        locy5 = 0.92
        space = Button(self.canvas, text='Space', width=40, font=('Arial', 12),
                       command=lambda: [self.press(' '), self.key_press_repeat(space_text, locy3, locy5)])
        space.place(relx=locy3, rely=locy5, anchor=CENTER)

    def end_keyboard(self, end):
        self.keys = self.keys + str(end)
        DS.write_to_from_keys(self.keys)
        self.keys = ""
        self.canvas.destroy()

    def display(self):
        self.get_keyboard()

    def clear(self):
        if len(self.keys) == 0:
            self.keys = " "
        self.keys = self.keys[:-1]
        DS.write_to_from_keys(self.keys)

    def shift(self):
        if not self.shift_lock:
            self.shift_lock = True
            self.canvas.itemconfig(self.name_text, text="UPPER CASE")
        else:
            self.shift_lock = False
            self.canvas.itemconfig(self.name_text, text="lower case")

    def press(self, key):
        if not self.shift_lock:
            self.keys = self.keys + str(key)
        else:
            cap = str(key).upper()
            self.keys = self.keys + cap
        DS.write_to_from_keys(self.keys)

    #############################################
    # Show the key repeat above the pressed key #
    #############################################
    def key_press_repeat(self, key, locx, locy):
        y = locy - 0.12
        width = 74
        height = 52
        if key == " ":
            width = 300
        upp = convert_key(key)
        show = Label(self.canvas, text=upp, font=("Arial", 16, "bold"), background="#FCF9BE", borderwidth=1,
                     relief="solid")
        show.place(width=width, height=height, relx=locx, rely=y, anchor=CENTER)
        Tk.update(self.canvas)
        sleep(0.2)
        show.destroy()

    #####################################
    # Display the keys to the canvas    #
    #####################################
    def display_keys(self, key, locx, locy):
        upp = convert_key(key)
        btn = Button(self.canvas, text=upp, width=7, font=("Arial", 12),
                     command=lambda: [self.press(key), self.key_press_repeat(key, locx, locy)])
        btn.place(relx=locx, rely=locy, anchor=CENTER)

    def remove_keyboard(self):
        self.canvas.destroy()
