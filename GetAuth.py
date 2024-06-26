"""
@author: Brian F
Creates an authentication pop-up screen to authorise admin actions without
leaving the testing area.
"""
from tkinter import Canvas, Label, Button
import OnScreenKeys
import SecurityManager

K = OnScreenKeys
KY = OnScreenKeys.Keyboard()
SM = SecurityManager.SecurityManager()

Authorise = False


def authenticate_user():
    global Authorise
    return Authorise


def set_auth(val):
    global Authorise
    Authorise = val


class GetAuth:
    def __init__(self):
        self.btn1 = None
        self.lab2 = None
        self.lab1 = None
        self.error = None
        self.auth_squ2 = None
        self.auth_squ1 = None
        self.auth_canvas = None
        self.clicked = False
        self.username = None
        self.password = None
        self.all_users = None
        self.back_colour = "#A7727D"

    def show_screen(self):
        self.auth_canvas = Canvas(bg=self.back_colour, width=500, height=280)
        self.auth_canvas.place(x=480, y=350)
        self.all_users = SM.GetUserList()
        self.setup()

    def setup(self):
        y = 70
        width = 300
        height = 40
        self.clicked = False
        Label(self.auth_canvas, text="Admin Authentication", background=self.back_colour,
              font=(K.FONT_NAME, 18, 'bold')).place(relx=0.2, rely=0.05)
        self.auth_squ1 = self.auth_canvas.create_rectangle(50, y, 50 + width, y + height, fill="#C2B6BF")
        self.lab1 = self.auth_canvas.create_text(90, 85)
        self.auth_canvas.itemconfig(self.lab1, text="Username", font=(K.FONT_NAME, 10, 'bold'))
        KY.get_keyboard()
        data_username = K.wait_for_response(self.auth_canvas, self.username, False, 0.45, 0.27)

        self.auth_squ2 = self.auth_canvas.create_rectangle(50, y + 80, 50 + width, y + 80 + height, fill="#C2B6BF")
        self.lab2 = self.auth_canvas.create_text(90, 158)
        self.auth_canvas.itemconfig(self.lab2, text="Password", font=(K.FONT_NAME, 10, 'bold'))
        KY.get_keyboard()
        data_password = K.wait_for_response(self.auth_canvas, self.password, True, 0.45, 0.55)

        self.username = data_username
        self.password = data_password
        cancel = Button(self.auth_canvas, text="Cancel", width=12, font=(K.FONT_NAME, 10, 'bold'), command=self.end)
        cancel.place(relx=0.4, rely=0.8)
        self.btn1 = Button(self.auth_canvas, text="Authenticate", width=14, height=2, background="#A6D1E6",
                           font=(K.FONT_NAME, 10, 'bold'),
                           command=self.task)
        self.btn1.place(relx=0.65, rely=0.78)
        self.auth_canvas.after(100, self.update())

    def end(self):
        self.auth_canvas.place_forget()
        self.auth_canvas.delete('all')
        self.auth_canvas.destroy()
        del self.auth_canvas

    def task(self):
        users = [(item.name, item.password) for item in self.all_users]
        for name, password in users:
            if self.username == name:
                if self.password == password:
                    set_auth(True)
        self.clicked = True
        self.end()

    def get_clicked(self):
        return self.clicked

    def update(self):
        pass
