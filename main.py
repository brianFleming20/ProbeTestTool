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

import UserLogin
import Sessions
import DeviceConnect
import ProbeTest
import AdminUser
import FaultFinder
import Connection
import AdminPortControl
import RetestProbe

UL = UserLogin
SE = Sessions
DC = DeviceConnect
PT = ProbeTest
AU = AdminUser
FF = FaultFinder
CO = Connection
AP = AdminPortControl
RT = RetestProbe

# define global variables
PTT_Version = 'Deltex Medical : P0035 Probe Test Tool V2.2'
w = 1000  # window width
h = 650  # window height
LARGE_FONT = ("Verdana", 14)


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


exp = " "


def press(num):
    global exp
    exp = exp + str(num)
    print(f"pressed {exp}")

def disable_event():
    pass


class WindowController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(PTT_Version)
        # get window width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # calculate x and y coordinates for the window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
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
                  RT.RetestProbe,
                  FF.FaultFindWindow):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # self.attributes('-fullscreen', True)
            # self.attributes('-toolwindow', True)
            # self.protocol("WM_DELETE_WINDOW", disable_event)
        self.show_frame(UL.LogInWindow)

        try:
            import pyi_splash
            pyi_splash.update_text('UI Loaded ...')
            pyi_splash.close()
        except:
            pass

    def show_frame(self, newFrame):
        frame = self.frames[newFrame]
        frame.tkraise()
        # Does the frame have a refresh method, if so call it.
        if hasattr(newFrame, 'refresh_window') and callable(getattr(newFrame, 'refresh_window')):
            self.frames[newFrame].refresh_window()


app = WindowController()
app.mainloop()
