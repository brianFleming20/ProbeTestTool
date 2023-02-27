"""Factory pattern for generating python beans"""
from tkinter import Canvas, Label, Button, Tk


def probe_canvas(self, message, btn):
    self.canvas_text = Canvas(bg="#eae9e9", width=350, height=180)
    self.canvas_text.place(relx=0.4, rely=0.5)
    Label(self.canvas_text, text=message, font=("Courier", 12)).place(
        x=50, y=20)
    btn1 = Button(self.canvas_text, text="Continue", command=self.yes_answer, width=10, height=2)
    btn2 = Button(self.canvas_text, text="Cancel", command=self.no_answer, width=10, height=2)
    Tk.update(self)
    while btn and self.info_canvas is None:
        btn1.place(x=90, y=120)
        btn2.place(x=190, y=120)
        Tk.update(self)


def text_destroy(self):
    self.canvas_text.destroy()


class Ports:
    def __init__(self, odm="", probe="", analyer="", move="", active=True):
        self.ODM = odm
        self.Probe = probe
        self.Analyser = analyer
        self.Move = move
        self.ODM_Active = active


class Location:
    def __init__(self, file):
        self.File = file


class Probes:
    def __init__(self, probe_type, current_batch, passed, left_to_test, failed=0, scrap=0):
        self.Probe_Type = probe_type
        self.Current_Batch = current_batch
        self.Passed = passed
        self.Left = left_to_test
        self.failed = failed
        self.scrap = scrap


class Users:
    def __init__(self, name, admin, plot=False, over_right=False, pw_user="", reset_password=False, non_human=False):
        self.Name = name
        self.Admin = admin
        self.Plot = plot
        self.Over_rite = over_right
        self.Change_password = pw_user
        self.reset_password = reset_password
        self.Non_Human = non_human


class User(object):
    ####################################################################################################
    # Used to create a user object, containing all the user`s info (username, password, admin status). #
    ####################################################################################################

    def __init__(self, name, password, admin=False):
        self.name = name
        self.password = password
        self.admin = admin


class Batch(object):
    ####################################
    # USed to create batch objects.    #
    ####################################

    def __init__(self, batchNumber=None):
        self.batchNumber = batchNumber
        self.probesProgrammed = 0
        self.batchQty = 0
        self.probe_type = ''
        self.serial_number = ''


class DeletedUser:

    def __int__(self, name, date):
        self.Name = name
        self.Date = date
