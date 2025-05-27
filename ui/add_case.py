import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import *
from database import insert_case

class AddCaseForm(Frame):
    def __init__(self, master):
        super().__init__(master, padding=0)
        self.pack(fill=BOTH, expand=YES)

        self.name_var = StringVar()
        self.date_var = StringVar()
        self.contact_var = StringVar()
        self.severity_var = StringVar()
        self.message_var = StringVar()

        Label(self, text="Add Case", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(15, 10), padx=30)

        form_outer = Frame(self, bootstyle="light", padding=20)
        form_outer.pack(fill=X, padx=30)
        form_outer.configure(borderwidth=1, relief="ridge")

        input_width = 52

        def field_label(text, row):
            lbl = Label(form_outer, text=text, font=("Segoe UI", 12, "bold"))
            lbl.grid(row=row, column=0, sticky=W, padx=(0, 10), pady=(6, 0))

        def entry_field(var, row):
            e = Entry(form_outer, textvariable=var, width=input_width)
            e.grid(row=row, column=1, sticky=W, pady=(6, 0))

        def dropdown_field(var, row):
            entry = Entry(form_outer, textvariable=var, width=input_width)
            entry.grid(row=row, column=1, sticky=W, pady=(6, 0))

            menu = tk.Menu(entry, tearoff=0)
            for option in ["Mild", "Moderate", "Severe"]:
                menu.add_command(label=option, command=lambda v=option: var.set(v))

            def show_menu(event):
                menu.tk_popup(event.x_root, event.y_root)

            entry.bind("<Button-1>", show_menu)

        field_label("Full Name", 0)
        entry_field(self.name_var, 0)

        field_label("Diagnosis Date (YYYY-MM-DD)", 1)
        entry_field(self.date_var, 1)

        field_label("Contact Info", 2)
        entry_field(self.contact_var, 2)

        field_label("Case Severity", 3)
        dropdown_field(self.severity_var, 3)

        save_btn = Button(
            form_outer,
            text="Save",
            bootstyle="info",
            width=input_width,
            padding=(4, 2),
            command=self.save_case
        )
        save_btn.grid(row=4, column=1, sticky=W, pady=(20, 5))

        self.status_label = Label(
            form_outer,
            textvariable=self.message_var,
            font=("Segoe UI", 10),
            bootstyle="success"
        )
        self.status_label.grid(row=5, column=1, sticky=W, pady=(0, 5))
        self.status_label.grid_remove()

        form_outer.columnconfigure(1, weight=1)

    def save_case(self):
        name = self.name_var.get().strip()
        date = self.date_var.get().strip()
        contact = self.contact_var.get().strip()
        severity = self.severity_var.get().strip()

        if all([name, date, contact, severity]):
            insert_case(name, date, contact, severity)
            self.message_var.set("Case added successfully")
            self.status_label.configure(bootstyle="success")
            self.status_label.grid()
            self.clear_form()
        else:
            self.message_var.set("Please fill out all fields")
            self.status_label.configure(bootstyle="danger")
            self.status_label.grid()

    def clear_form(self):
        self.name_var.set("")
        self.date_var.set("")
        self.contact_var.set("")
        self.severity_var.set("")
