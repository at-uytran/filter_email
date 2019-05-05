import pandas as pd
from os import path

class MailBox():
    def __init__(self):
        if (path.exists("spams.csv") == True):
            self.spams_box = pd.read_csv('spams.csv', header=0)
        else:
            self.spams_box = ""

        if (path.exists("hams.csv") == True):
            self.hams_box = pd.read_csv('hams.csv', header=0)
        else:
            self.hams_box = ""

    def get_spams(self):
        result_spams = ""
        result_spams += "{}".format(self.spams_box)
        return result_spams

    def get_hams(self):
        result_hams = ""
        result_hams += "{}".format(self.hams_box)
        return result_hams
