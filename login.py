import pandas as pd
from filter_class import FilterEmail
from mail_box import MailBox
# Import For gui
from tkinter import Tk, N, S, W, E, END, Text, BOTH, StringVar
from tkinter.ttk import Frame, Button, Entry, Style, Label
from os import path
import threading

ACCOUNT = "tu"
PASSWORD = "tu"

class GUI(Frame):
    def __init__(self):
        super().__init__()

        self.infomation_frame = Frame()
        self.login_frame = Frame()
        self.system_frame = Frame()

        self.init_information()

        self.filter = FilterEmail()

    def init_information(self):
        self.infomation_frame.master.title("Email filter app")
        self.infomation_frame.master.geometry("%sx%s+%s+%s" % (1000, 1000, 1, 1))
        Style().configure("TButton", padding=(0, 5, 0, 5),
                          font='serif 10')
        self.infomation_frame.columnconfigure(0, pad=10)
        self.infomation_frame.rowconfigure(0, pad=10)
        self.infomation_frame.rowconfigure(1, pad=10)

        self.btn_to_login = Button(self.infomation_frame, text='To system', command=self.load_login_UI, width="25")
        self.information_content= Text(self.infomation_frame, height=10, width=10)
        self.information_content.grid(row=0, column=0)
        self.btn_to_login.grid(row=1, column=0)
        self.information_content .insert(END, "Content to add")


        self.infomation_frame.pack(fill=BOTH, expand=1)

    def write_data_spams(self, array):
        if (path.exists("spams.csv") == True):
            df = pd.DataFrame(data=[array])
            df.to_csv("spams.csv", index=False, header=False, encoding="utf-8", mode='a')
        else:
            df = pd.DataFrame(data=[array], columns=['text'])
            df.to_csv("spams.csv", index=False, encoding="utf-8", mode='a')

    def write_data_hams(self, array):
        if (path.exists("hams.csv") == True):
            df = pd.DataFrame(data=[array])
            df.to_csv("hams.csv", index=False, header=False, encoding="utf-8", mode='a')
        else:
            df = pd.DataFrame(data=[array], columns=['text'])
            df.to_csv("hams.csv", index=False, encoding="utf-8", mode='a')

    def load_login_UI(self):
        self.infomation_frame.destroy()
        self.login_frame.master.title("Email filter app")
        self.login_frame.master.geometry("%sx%s+%s+%s" % (250, 150, 500, 250))
        Style().configure("TButton", padding=(0, 5, 0, 5),
                          font='serif 10')

        self.login_frame.columnconfigure(0, pad=10)
        self.login_frame.columnconfigure(1, pad=10)

        self.login_frame.rowconfigure(0, pad=10)
        self.login_frame.rowconfigure(1, pad=10)
        self.login_frame.rowconfigure(2, pad=10)

        self.account_label = Label(self.login_frame, text="Account:")
        self.account = Entry(self.login_frame)
        self.account_label.grid(row=0, column=0)
        self.account.grid(row=0, column=1)

        self.pass_word_label = Label(self.login_frame, text="Password:")
        self.password = Entry(self.login_frame, show="*")
        self.pass_word_label.grid(row=1, column=0)
        self.password.grid(row=1, column=1)

        self.btn_login = Button(self.login_frame, text='Login', command=self.login, width="25")
        self.btn_login.grid(row=2, columnspan=2)
        self.login_frame.pack(fill=BOTH, expand=1)

    def login(self):
        account = self.account.get()
        password = self.password.get()
        if (account == ACCOUNT and password == PASSWORD):
            self.login_frame.destroy()
            self.load_main_UI()
            self.refresh_boxes()

    def load_main_UI(self):
        self.emails = pd.read_csv('emails.csv', header=0)
        self.system_frame.master.title("Email filter app")
        self.system_frame.master.geometry("%sx%s+%s+%s" % (1390, 1080, 0, 0))
        Style().configure("TButton", padding=(0, 5, 0, 5),
                          font='serif 10')

        self.system_frame.columnconfigure(0, pad=10)
        self.system_frame.columnconfigure(1, pad=10)
        self.system_frame.columnconfigure(2, pad=10)
        self.system_frame.columnconfigure(3, pad=10)
        self.system_frame.columnconfigure(4, pad=10)
        self.system_frame.columnconfigure(5, pad=10)

        self.system_frame.rowconfigure(0, pad=10)
        self.system_frame.rowconfigure(1, pad=10)
        self.system_frame.rowconfigure(2, pad=10)
        self.system_frame.rowconfigure(3, pad=10)

        self.btn_read_mail = Button(self.system_frame, text='Read email', command=self.read_email, width="25")
        self.btn_read_mail.grid(row=0, column=0)

        self.result_read_mail = Text(self.system_frame, height=5, width=150)
        self.result_read_mail.grid(columnspan=5, row=0, column=1)

        self.btn_process_data = Button(self.system_frame, text='Process data', command=self.process_data)
        self.btn_process_data .grid(row=1, column=0)

        self.result_process_data = Text(self.system_frame, height=5, width=150)
        self.result_process_data.grid(columnspan=5, row=1, column=1)

        self.btn_filter_emails = Button(self.system_frame, text='Filter emails', command=self.filter_emails)
        self.btn_filter_emails.grid(row=2, column=0)

        self.result_filter_emails = Text(self.system_frame, height=5, width=150)
        self.result_filter_emails.grid(columnspan=5, row=2, column=1)


        self.id_email = StringVar()
        self.email_id_for_check = Entry(self.system_frame, textvariable=self.id_email)
        # self.email_id_for_check = Text(self, height=10, width=10)
        self.email_id_for_check.grid(row=3, column=1)

        self.btn_check_email = Button(self.system_frame, text='Check email', command=self.check_email, width="15")
        self.btn_check_email.grid(row=3, column=0)

        self.label_email_content = Label(self.system_frame, text="Email content:")
        self.email_content = Text(self.system_frame, height=10, width=20)
        self.label_result_check_mail = Label(self.system_frame, text="Email type:")
        self.result_check_mail = Text(self.system_frame, height=5, width=20)

        self.label_email_content.grid(row=3, column=2)
        self.email_content.grid(row=3, column=3)
        self.label_result_check_mail.grid(row=3, column=4)
        self.result_check_mail.grid(row=3, column=5)

        self.label_mail_boxes = Label(self.system_frame, text="Mail boxes:")
        self.label_spam_list= Label(self.system_frame, text="Spam box:")
        self.label_inbox_list= Label(self.system_frame, text="Inbox:")
        self.list_spam_box = Text(self.system_frame, height=10, width=45)
        self.list_inbox = Text(self.system_frame, height=10, width=45)

        self.label_mail_boxes.grid(row=5, column=0)
        self.label_spam_list.grid(row=4, column=1, columnspan=2)
        self.label_inbox_list.grid(row=4, column=3, columnspan=2)
        self.list_spam_box.grid(row=5, column=1, columnspan=2)
        self.list_inbox.grid(row=5, column=3, columnspan=2)

        self.system_frame.pack(fill=BOTH, expand=1)

    def refresh_boxes(self):
        mail_box = MailBox()

        self.list_spam_box.delete('1.0', END)
        self.list_inbox.delete('1.0', END)

        list_spams = mail_box.get_spams()
        list_hams = mail_box.get_hams()
        self.list_spam_box.insert(END, list_spams)
        self.list_inbox.insert(END, list_hams)

    def read_email(self):
        result_log = self.filter.initialize_emails_and_data()
        self.result_read_mail.insert(END, result_log)

    def process_data(self):
        resutlt_log = self.filter.process_data()
        self.result_process_data .insert(END, resutlt_log)

    def filter_emails(self):
        result_log = self.filter.filter_emails()
        self.result_filter_emails.insert(END, result_log)

    def check_email(self):
        email_id = int(self.email_id_for_check.get())
        self.set_email_content(self.emails['text'][email_id])

        if self.filter.filter_by_id(email_id) == 1:
            email_type = "spam"
            self.write_data_spams([self.emails['text'][email_id]])
        else:
            email_type = "ham"
            self.write_data_hams([self.emails['text'][email_id]])

        self.set_email_type(email_type)

        self.refresh_boxes()

    def set_email_content(self, content):
        self.email_content.delete("1.0", END)
        self.email_content.insert(END, content)

    def set_email_type(self, type):
        self.result_check_mail.delete("1.0", END)
        self.result_check_mail.insert(END, type)

def main():
    root = Tk()
    GUI()
    root.mainloop()

main()
