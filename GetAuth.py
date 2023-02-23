from tkinter import *
import OnScreenKeys
import SecurityManager

K = OnScreenKeys
KY = OnScreenKeys.Keyboard()
SM = SecurityManager.SecurityManager()

Authorise = False


def get_authorise():
    return Authorise


class GetAuth():
    def __init__(self):
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
        self.back_colour = "#FCFFE7"

    def show_screen(self):
        self.auth_canvas = Canvas(bg=self.back_colour, width=500, height=280)
        self.auth_canvas.place(x=420, y=350)
        self.all_users = SM.GetUserList()
        self.setup()

    def setup(self):
        y = 70
        width = 300
        height = 40
        self.clicked = False
        Label(self.auth_canvas, text="Admin Authentication", font=(K.FONT_NAME, 18, 'bold')).place(relx=0.2, rely=0.05)
        self.error = self.auth_canvas.create_text(150, 120)
        self.auth_squ1 = self.auth_canvas.create_rectangle(50, y, 50 + width, y + height, fill="#C2B6BF")
        self.lab1 = self.auth_canvas.create_text(90, 85)
        self.auth_canvas.itemconfig(self.lab1, text="Username", font=(K.FONT_NAME, 10, 'bold'))
        # KY.get_keyboard()
        # data_username = K.wait_for_response(self.auth_canvas, self.username, False, 0.45, 0.27)

        self.auth_squ2 = self.auth_canvas.create_rectangle(50, y + 80, 50 + width, y + 80 + height, fill="#C2B6BF")
        self.lab2 = self.auth_canvas.create_text(90, 158)
        self.auth_canvas.itemconfig(self.lab2, text="Password", font=(K.FONT_NAME, 10, 'bold'))
        # KY.get_keyboard()
        # data_password = K.wait_for_response(self.auth_canvas, self.password, True, 0.45, 0.55)

        # self.username = data_username
        # self.password = data_password
        self.username = "brian"
        self.password = "pass"
        cancel = Button(self.auth_canvas, text="Cancel", width=12, font=(K.FONT_NAME, 10, 'bold'), command=self.end)
        cancel.place(relx=0.4, rely=0.8)
        btn1 = Button(self.auth_canvas, text="Authenticate", width=14, background="#A6D1E6", font=(K.FONT_NAME, 10, 'bold'),
                      command=self.end)
        btn1.focus
        btn1.place(relx=0.65, rely=0.8)
        btn1.bind('<Button-1>', self.task)

    def end(self):
        self.auth_canvas.destroy()

    def authenticate_user(self):
        global Authorise
        return Authorise

    def task(self, event):
        self.auth_canvas.itemconfig(self.error, text="Authenticating", font=(K.FONT_NAME, 14, 'bold'))
        users = [(item.name, item.password) for item in self.all_users]
        for name, password in users:
            if self.username == name:
                if self.password == password:
                    self.set_auth(True)
        self.clicked = True
        self.auth_canvas.delete(self.auth_squ1)
        self.auth_canvas.delete(self.auth_squ2)
        self.auth_canvas.delete(self.lab1)
        self.auth_canvas.delete(self.lab2)

    def get_clicked(self):
        return self.clicked

    def set_auth(self, val):
        global Authorise
        Authorise = val


