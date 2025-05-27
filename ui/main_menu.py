import tkinter as tk
from ttkbootstrap import Frame, Button, Label, Style
from ttkbootstrap.constants import *
from ui.add_case import AddCaseForm
from ui.view_cases import ViewCases
from ui.reports import Reports
from ui.settings import Settings

class MainMenu(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.sidebar = Frame(self, width=200, style="primary.TFrame")
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        Label(
            self.sidebar,
            text="HIV/AIDS Case\nManagement System",
            font=("Segoe UI", 16, "bold"),
            style="primary.Inverse.TLabel",
            justify="center",
            anchor="center"
        ).pack(pady=(20, 10), padx=10)

        self.buttons = {}
        menu_items = ["Add Case", "View Cases", "Reports", "Settings"]
        for item in menu_items:
            btn = Button(
                self.sidebar,
                text=item,
                bootstyle="primary",
                width=20,
                command=lambda i=item: self.load_frame(i)
            )
            btn.pack(anchor=NW, pady=5, padx=10)
            self.buttons[item] = btn

        tk.Frame(self.sidebar, height=1, bg="#ccc").pack(fill=X, padx=10, pady=15)

        Button(
            self.sidebar,
            text="Logout",
            bootstyle="light",
            width=20,
            command=self.logout
        ).pack(side=BOTTOM, pady=10, padx=10, anchor=SW)

        self.content = Frame(self, padding=0)
        self.content.pack(side=LEFT, fill=BOTH, expand=YES)

        self.active_frame = None
        self.load_frame("Add Case")

    def load_frame(self, name):
        if self.active_frame:
            self.active_frame.destroy()

        if name == "Add Case":
            self.active_frame = AddCaseForm(self.content)
        elif name == "View Cases":
            self.active_frame = ViewCases(self.content)
        elif name == "Reports":
            self.active_frame = Reports(self.content)
        elif name == "Settings":
            self.active_frame = Settings(self.content)
        else:
            self.active_frame = Frame(self.content)
            Label(
                self.active_frame,
                text=f"{name} Page",
                font=("Segoe UI", 14)
            ).pack(pady=20)

        self.active_frame.pack(fill=BOTH, expand=YES)

    def logout(self):
        self.master.destroy()
