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



_TITLE="This is the title"
PTT_Version = 'canvasboard By Danish' # title Name
GREEN = "#9bdeac"
FONT_NAME = "Courier"

# showing all data in display 

class Keyboard():
    def __init__(self):
      self.keys = "///"
# First Line Button
    def get_keyboard(self):   
        canvas = Canvas(width=1010, height=200) 
        
         
        q = ttk.Button(canvas,text = 'Q' , width = 9, command = lambda : self.press('Q'))
        q.place(relx=0.13, rely=0.1 ,anchor=CENTER)

        w = ttk.Button(canvas,text = 'W' , width = 9, command = lambda : self.press('W'))
        w.place(relx=0.20, rely=0.1, anchor=CENTER)

        e = ttk.Button(canvas,text = 'E' , width = 9, command = lambda : self.press('E'))
        e.place(relx=0.27, rely=0.1, anchor=CENTER)

        R = ttk.Button(canvas,text = 'R' , width = 9, command = lambda : self.press('R'))
        R.place(relx=0.34, rely=0.1, anchor=CENTER)

        T = ttk.Button(canvas,text = 'T' , width = 9, command = lambda : self.press('T'))
        T.place(relx=0.41, rely=0.1, anchor=CENTER)

        Y = ttk.Button(canvas,text = 'Y' , width = 9, command = lambda : self.press('Y'))
        Y.place(relx=0.48, rely=0.1, anchor=CENTER)

        U = ttk.Button(canvas,text = 'U' , width = 9, command = lambda : self.press('U'))
        U.place(relx=0.55, rely=0.1, anchor=CENTER)

        I = ttk.Button(canvas,text = 'I' , width = 9, command = lambda : self.press('I'))
        I.place(relx=0.62, rely=0.1, anchor=CENTER)

        O = ttk.Button(canvas,text = 'O' , width = 9, command = lambda : self.press('O'))
        O.place(relx=0.69, rely=0.1, anchor=CENTER)

        P = ttk.Button(canvas,text = 'P' , width = 9, command = lambda : self.press('P'))
        P.place(relx=0.76, rely=0.1, anchor=CENTER)

        clear = ttk.Button(canvas,text = 'Clear' , width = 9, command = self.clear)
        clear.place(relx=0.83, rely=0.1, anchor=CENTER)

        

       # Second Line Button



        A = ttk.Button(canvas,text = 'A' , width = 9, command = lambda : self.press('A'))
        A.place(relx=0.15, rely=0.22, anchor=CENTER)


        S = ttk.Button(canvas,text = 'S' , width = 9, command = lambda : self.press('S'))
        S.place(relx=0.22, rely=0.22, anchor=CENTER)

        D = ttk.Button(canvas,text = 'D' , width = 9, command = lambda : self.press('D'))
        D.place(relx=0.29, rely=0.22, anchor=CENTER)

        F = ttk.Button(canvas,text = 'F' , width = 9, command = lambda : self.press('F'))
        F.place(relx=0.36, rely=0.22, anchor=CENTER)


        G = ttk.Button(canvas,text = 'G' , width = 9, command = lambda : self.press('G'))
        G.place(relx=0.43, rely=0.22, anchor=CENTER)


        H = ttk.Button(canvas,text = 'H' , width = 9, command = lambda : self.press('H'))
        H.place(relx=0.5, rely=0.22, anchor=CENTER)


        J = ttk.Button(canvas,text = 'J' , width = 9, command = lambda : self.press('J'))
        J.place(relx=0.57, rely=0.22, anchor=CENTER)


        K = ttk.Button(canvas,text = 'K' , width = 9, command = lambda : self.press('K'))
        K.place(relx=0.64, rely=0.22, anchor=CENTER)

        L = ttk.Button(canvas,text = 'L' , width = 9, command = lambda : self.press('L'))
        L.place(relx=0.71, rely=0.22, anchor=CENTER)


        semi_co = ttk.Button(canvas,text = ';' , width = 9, command = lambda : self.press(';'))
        semi_co.place(relx=0.78, rely=0.22, anchor=CENTER)
  


        enter = ttk.Button(canvas,text = 'Enter' , width = 12, command = self.action)
        enter.place(relx=0.85, rely=0.22, anchor=CENTER)

        # third line Button

        Z = ttk.Button(canvas,text = 'Z' , width = 9, command = lambda : self.press('Z'))
        Z.place(relx=0.18, rely=0.34, anchor=CENTER)


        X = ttk.Button(canvas,text = 'X' , width = 9, command = lambda : self.press('X'))
        X.place(relx=0.25, rely=0.34, anchor=CENTER)


        C = ttk.Button(canvas,text = 'C' , width = 9, command = lambda : self.press('C'))
        C.place(relx=0.32, rely=0.34, anchor=CENTER)


        V = ttk.Button(canvas,text = 'V' , width = 9, command = lambda : self.press('V'))
        V.place(relx=0.39, rely=0.34, anchor=CENTER)

        B = ttk.Button(canvas, text= 'B' , width = 9 , command = lambda : self.press('B'))
        B.place(relx=0.46, rely=0.34, anchor=CENTER)


        N = ttk.Button(canvas,text = 'N' , width = 9, command = lambda : self.press('N'))
        N.place(relx=0.53, rely=0.34, anchor=CENTER)


        M = ttk.Button(canvas,text = 'M' , width = 9, command = lambda : self.press('M'))
        M.place(relx=0.6, rely=0.34, anchor=CENTER)


        slas = ttk.Button(canvas,text = '/' , width = 9, command = lambda : self.press('/'))
        slas.place(relx=0.67, rely=0.34, anchor=CENTER)


        q_mark = ttk.Button(canvas,text = '?' , width = 9, command = lambda : self.press('?'))
        q_mark.place(relx=0.74, rely=0.34, anchor=CENTER)


        coma = ttk.Button(canvas,text = '.' , width = 9, command = lambda : self.press('.'))
        coma.place(relx=0.81, rely=0.34, anchor=CENTER)
       

        shift = ttk.Button(canvas,text = 'Shift' , width = 9, command = lambda : self.press('Shift'))
        shift.place(relx=0.88, rely=0.34, anchor=CENTER)

        #Fourth Line Button


        space = ttk.Button(canvas,text = 'Space' , width = 40, command = lambda : self.press(' '))
        space.place(relx=0.5, rely=0.45, anchor=CENTER)
      
      
        end = ttk.Button(canvas, text="Finish with Keys", width=20, command= lambda : canvas.destroy())
        end.place(relx=0.8, rely=0.5, anchor=CENTER)
        canvas.pack()
        return self.keys
    
    
  
    def clear(self):
        pass
        # equation.set(exp)
        
    def action(self):
        pass
        # equation.set(exp)
        
   
   
    def press(self,num):
        self.keys = self.keys + str(num)
        print(f"press {self.keys}")
        # every keyboard press chould be recoreded in the datastore for use in the system.
       