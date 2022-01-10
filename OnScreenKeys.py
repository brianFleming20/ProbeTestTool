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


import datastore
from tkinter import *
from tkinter import ttk




_TITLE="This is the title"
PTT_Version = 'self.canvasboard By Danish' # title Name
GREEN = "#9bdeac"
FONT_NAME = "Courier"
DS = datastore.DataStore()

# showing all data in display 

class Keyboard():
    def __init__(self):
      self.keys = ""
      
# First Line Button
    def get_keyboard(self): 
        self.keystrokes = StringVar()  
        self.shift_lock = False
        self.canvas = Canvas(width=1010, height=240) 
        ttk.Label(self.canvas, textvariable=self.keystrokes, relief=SUNKEN, font="bold",
                  width=30).place(relx=0.4, rely=0.1, anchor='w')
        
        # Numbers section
        self.name_text = self.canvas.create_text(150,20,text="lower case",fill="black",font=(FONT_NAME, 12, "bold"))
        one = ttk.Button(self.canvas,text = '1' , width = 9, command = lambda : self.press('1'))
        one.place(relx=0.15, rely=0.18 ,anchor=CENTER)
        
        two = ttk.Button(self.canvas,text = '2' , width = 9, command = lambda : self.press('2'))
        two.place(relx=0.22, rely=0.18 ,anchor=CENTER)
        
        three = ttk.Button(self.canvas,text = '3' , width = 9, command = lambda : self.press('3'))
        three.place(relx=0.29, rely=0.18 ,anchor=CENTER)
        
        four = ttk.Button(self.canvas,text = '4' , width = 9, command = lambda : self.press('4'))
        four.place(relx=0.36, rely=0.18 ,anchor=CENTER)
        
        five = ttk.Button(self.canvas,text = '5' , width = 9, command = lambda : self.press('5'))
        five.place(relx=0.43, rely=0.18 ,anchor=CENTER)
        
        six = ttk.Button(self.canvas,text = '6' , width = 9, command = lambda : self.press('6'))
        six.place(relx=0.5, rely=0.18 ,anchor=CENTER)
        
        seven = ttk.Button(self.canvas,text = '7' , width = 9, command = lambda : self.press('7'))
        seven.place(relx=0.57, rely=0.18 ,anchor=CENTER)
        
        eight = ttk.Button(self.canvas,text = '8' , width = 9, command = lambda : self.press('8'))
        eight.place(relx=0.64, rely=0.18 ,anchor=CENTER)
        
        nine = ttk.Button(self.canvas,text = '9' , width = 9, command = lambda : self.press('9'))
        nine.place(relx=0.71, rely=0.18 ,anchor=CENTER)
        
        zero = ttk.Button(self.canvas,text = '0' , width = 9, command = lambda : self.press('0'))
        zero.place(relx=0.78, rely=0.18 ,anchor=CENTER)
        
        # Frist letter row
        q = ttk.Button(self.canvas,text = 'Q' , width = 9, command = lambda : self.press('q'))
        q.place(relx=0.13, rely=0.3 ,anchor=CENTER)

        w = ttk.Button(self.canvas,text = 'W' , width = 9, command = lambda : self.press('w'))
        w.place(relx=0.20, rely=0.3, anchor=CENTER)

        e = ttk.Button(self.canvas,text = 'E' , width = 9, command = lambda : self.press('e'))
        e.place(relx=0.27, rely=0.3, anchor=CENTER)

        R = ttk.Button(self.canvas,text = 'R' , width = 9, command = lambda : self.press('r'))
        R.place(relx=0.34, rely=0.3, anchor=CENTER)

        T = ttk.Button(self.canvas,text = 'T' , width = 9, command = lambda : self.press('t'))
        T.place(relx=0.41, rely=0.3, anchor=CENTER)

        Y = ttk.Button(self.canvas,text = 'Y' , width = 9, command = lambda : self.press('y'))
        Y.place(relx=0.48, rely=0.3, anchor=CENTER)

        U = ttk.Button(self.canvas,text = 'U' , width = 9, command = lambda : self.press('u'))
        U.place(relx=0.55, rely=0.3, anchor=CENTER)

        I = ttk.Button(self.canvas,text = 'I' , width = 9, command = lambda : self.press('i'))
        I.place(relx=0.62, rely=0.3, anchor=CENTER)

        O = ttk.Button(self.canvas,text = 'O' , width = 9, command = lambda : self.press('o'))
        O.place(relx=0.69, rely=0.3, anchor=CENTER)

        P = ttk.Button(self.canvas,text = 'P' , width = 9, command = lambda : self.press('p'))
        P.place(relx=0.76, rely=0.3, anchor=CENTER)

        clear = ttk.Button(self.canvas,text = 'Clear' , width = 9, command = self.clear)
        clear.place(relx=0.83, rely=0.3, anchor=CENTER)

       # Second Letter Line

        A = ttk.Button(self.canvas,text = 'A' , width = 9, command = lambda : self.press('a'))
        A.place(relx=0.15, rely=0.42, anchor=CENTER)


        S = ttk.Button(self.canvas,text = 'S' , width = 9, command = lambda : self.press('s'))
        S.place(relx=0.22, rely=0.42, anchor=CENTER)

        D = ttk.Button(self.canvas,text = 'D' , width = 9, command = lambda : self.press('d'))
        D.place(relx=0.29, rely=0.42, anchor=CENTER)

        F = ttk.Button(self.canvas,text = 'F' , width = 9, command = lambda : self.press('f'))
        F.place(relx=0.36, rely=0.42, anchor=CENTER)


        G = ttk.Button(self.canvas,text = 'G' , width = 9, command = lambda : self.press('g'))
        G.place(relx=0.43, rely=0.42, anchor=CENTER)


        H = ttk.Button(self.canvas,text = 'H' , width = 9, command = lambda : self.press('h'))
        H.place(relx=0.5, rely=0.42, anchor=CENTER)


        J = ttk.Button(self.canvas,text = 'J' , width = 9, command = lambda : self.press('J'))
        J.place(relx=0.57, rely=0.42, anchor=CENTER)


        K = ttk.Button(self.canvas,text = 'K' , width = 9, command = lambda : self.press('k'))
        K.place(relx=0.64, rely=0.42, anchor=CENTER)

        L = ttk.Button(self.canvas,text = 'L' , width = 9, command = lambda : self.press('l'))
        L.place(relx=0.71, rely=0.42, anchor=CENTER)


        semi_co = ttk.Button(self.canvas,text = ';' , width = 9, command = lambda : self.press(';'))
        semi_co.place(relx=0.78, rely=0.42, anchor=CENTER)
  


        enter = ttk.Button(self.canvas,text = 'Enter' , width = 16, command = self.action)
        enter.place(relx=0.88, rely=0.42, anchor=CENTER)

        # third line Button

        Z = ttk.Button(self.canvas,text = 'Z' , width = 9, command = lambda : self.press('z'))
        Z.place(relx=0.18, rely=0.54, anchor=CENTER)


        X = ttk.Button(self.canvas,text = 'X' , width = 9, command = lambda : self.press('x'))
        X.place(relx=0.25, rely=0.54, anchor=CENTER)


        C = ttk.Button(self.canvas,text = 'C' , width = 9, command = lambda : self.press('c'))
        C.place(relx=0.32, rely=0.54, anchor=CENTER)


        V = ttk.Button(self.canvas,text = 'V' , width = 9, command = lambda : self.press('v'))
        V.place(relx=0.39, rely=0.54, anchor=CENTER)

        B = ttk.Button(self.canvas, text= 'B' , width = 9 , command = lambda : self.press('b'))
        B.place(relx=0.46, rely=0.54, anchor=CENTER)


        N = ttk.Button(self.canvas,text = 'N' , width = 9, command = lambda : self.press('n'))
        N.place(relx=0.53, rely=0.54, anchor=CENTER)


        M = ttk.Button(self.canvas,text = 'M' , width = 9, command = lambda : self.press('m'))
        M.place(relx=0.6, rely=0.54, anchor=CENTER)


        slas = ttk.Button(self.canvas,text = '/' , width = 9, command = lambda : self.press('/'))
        slas.place(relx=0.67, rely=0.54, anchor=CENTER)


        q_mark = ttk.Button(self.canvas,text = '?' , width = 9, command = lambda : self.press('?'))
        q_mark.place(relx=0.74, rely=0.54, anchor=CENTER)


        coma = ttk.Button(self.canvas,text = '.' , width = 9, command = lambda : self.press('.'))
        coma.place(relx=0.81, rely=0.54, anchor=CENTER)
       

        shift = ttk.Button(self.canvas,text = 'Shift Lock' , width = 9, command = lambda : self.shift())
        shift.place(relx=0.88, rely=0.54, anchor=CENTER)

        #Fourth Line Button


        space = ttk.Button(self.canvas,text = 'Space' , width = 40, command = lambda : self.press(' '))
        space.place(relx=0.5, rely=0.68, anchor=CENTER)
        
        
        end = ttk.Button(self.canvas, text="Finish with Keys", width=20, command= lambda check = '+': [self.end_keyboard(check),self.canvas.destroy()])
        end.place(relx=0.8, rely=0.76, anchor=CENTER)

        self.canvas.pack()
        
    def end_keyboard(self, end):
        self.keys = self.keys + str(end)
        DS.write_to_from_keys(self.keys)
        self.keys = ""
        
        
    def display(self):
        self.get_keyboard()
        
        
  
    def clear(self):
        self.keys = self.keys[:-1]
        DS.write_to_from_keys(self.keys)
    
        
    def action(self):
        DS.write_to_from_keys(self.keys)

        
    def shift(self):
        if self.shift_lock == False:
            self.shift_lock = True
            self.canvas.itemconfig(self.name_text, text="UPPER CASE")
        else:
            self.shift_lock = False
            self.canvas.itemconfig(self.name_text, text="lower case")
   
   
    def press(self,num):
        if self.shift_lock == False:
            self.keys = self.keys + str(num)
        else:
            cap = str(num).upper()
            self.keys = self.keys + cap
            
      
        DS.write_to_from_keys(self.keys)
        self.keystrokes.set(self.keys)
        # every keyboard press chould be recoreded in the datastore for use in the system.
       