'''Factory pattern for generating python beans'''

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
    def __init__(self, probe_type, current_batch, passed, tested, failed=0, scrap=0):
        self.Probe_Type = probe_type
        self.Current_Batch = current_batch
        self.Passed = passed
        self.Left = tested
        self.failed = failed
        self.scrap = scrap


class Users:
    def __init__(self, name, admin, plot=False, over_right=False, pw_user="", reset_password=False):
        self.Name = name
        self.Admin = admin
        self.Plot = plot
        self.Over_rite = over_right
        self.Change_password = pw_user
        self.reset_password = reset_password
