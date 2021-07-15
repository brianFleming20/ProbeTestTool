'''
Created on 3 May 2017

@author: jackw
@amended by Brian F

Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function

Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial


to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list

#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))

'''
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
from tkinter import filedialog




import UserLogin as UL
import Sessions as SE
import DeviceConnect as DC
import ProbeTest as PT
import AdminUser as AU
import FaultFinder as FF
import Connection as CO
import AdminPortControl as AP



# define global variables
PTT_Version = 'Deltex Medical : P0035 Probe Test Tool V1.0'
w = 1000  # window width
h = 650  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


class WindowController(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title(PTT_Version)
        # get window width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        
        for F in (UL.LogInWindow,
                  SE.SessionSelectWindow,
                  SE.NewSessionWindow,
                  SE.ContinueSessionWindow,
                  DC.ConnectionWindow,
                  DC.ConnectionAdmin,
                  CO.Connection,
                  AU.AdminWindow,
                  AU.AddUserWindow,
                  AP.AdminPorts,
                  AU.ChangePasswordWindow,
                  AU.EditUserWindow,
                  PT.TestProgramWindow,
                  FF.FaultFindWindow):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            # self.attributes('-fullscreen', True)

        self.show_frame(UL.LogInWindow)
       

    def show_frame(self, newFrame):

        frame = self.frames[newFrame]
        frame.tkraise()

        # Does the frame have a refresh method, if so call it.
        if hasattr(newFrame, 'refresh_window') and callable(getattr(newFrame, 'refresh_window')):
            self.frames[newFrame].refresh_window()







              

app = WindowController()
app.mainloop()
