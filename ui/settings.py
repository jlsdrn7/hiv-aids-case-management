import tkinter as tk
from ttkbootstrap import Frame, Label, Combobox, StringVar, Button
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

class Settings(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(self, text="Settings", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 20))

        Label(self, text="Select Theme", font=("Segoe UI", 11, "bold")).pack(anchor=NW)
        self.theme_var = StringVar()
        self.style = Style()
        themes = self.style.theme_names()
        self.theme_var.set(self.style.theme.name)

        theme_combo = Combobox(self, textvariable=self.theme_var, values=themes, state="readonly", width=30)
        theme_combo.pack(anchor=NW, pady=(5, 15))
        Button(self, text="Apply Theme", bootstyle="primary", command=self.change_theme).pack(anchor=NW)

        Label(self, text="About", font=("Segoe UI", 11, "bold")).pack(anchor=NW, pady=(30, 5))
        info = (
            "HIV/AIDS Case Management System\n"
            "Version 1.0.0\n"
            "© 2024 Your Organization"
        )
        Label(self, text=info, font=("Segoe UI", 10)).pack(anchor=NW)

    def change_theme(self):
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)
