import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import *

class LoginScreen(Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.username = StringVar()
        self.password = StringVar()
        self.on_success = on_success

        wrapper = Frame(self)
        wrapper.place(relx=0.5, rely=0.5, anchor=CENTER)

        login_box = Frame(wrapper, padding=20, bootstyle="light")
        login_box.pack()

        Label(login_box, text="Login", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        Label(login_box, text="Username").grid(row=1, column=0, sticky=W, pady=5)
        Entry(login_box, textvariable=self.username, width=30).grid(row=1, column=1, pady=5)

        Label(login_box, text="Password").grid(row=2, column=0, sticky=W, pady=5)
        Entry(login_box, textvariable=self.password, show="*", width=30).grid(row=2, column=1, pady=5)

        Button(login_box, text="Login", bootstyle="primary", width=30, command=self.attempt_login).grid(row=3, column=0, columnspan=2, pady=(15, 0))

    def attempt_login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if user == "admin" and pwd == "1234":
            self.on_success()
        else:
            from tkinter import messagebox
            messagebox.showerror("Login Failed", "Invalid username or password.")
