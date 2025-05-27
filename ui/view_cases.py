import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, Combobox, StringVar, Scrollbar, Toplevel
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, filedialog
import csv
from database import fetch_all_cases, update_case, delete_case_by_id

class ViewCases(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        self.search_var = StringVar()
        self.severity_filter = StringVar()

        Label(self, text="View Cases", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 10))

        filter_frame = Frame(self)
        filter_frame.pack(fill=X, pady=(0, 10))

        Entry(filter_frame, textvariable=self.search_var, width=30).pack(side=LEFT, padx=(0, 10))
        Combobox(filter_frame, textvariable=self.severity_filter, values=["", "Mild", "Moderate", "Severe"], width=15, state="readonly").pack(side=LEFT)

        Button(filter_frame, text="Search", bootstyle="primary", command=self.apply_filters).pack(side=LEFT, padx=10)
        Button(filter_frame, text="Reset", bootstyle="secondary", command=self.reset_filters).pack(side=LEFT)
        Button(filter_frame, text="Export CSV", bootstyle="secondary-outline", command=self.export_csv).pack(side=LEFT, padx=10)

        action_frame = Frame(self)
        action_frame.pack(fill=X, pady=(0, 10))
        Button(action_frame, text="Edit Selected", bootstyle="warning-outline", command=self.edit_selected).pack(side=LEFT, padx=(0, 10))
        Button(action_frame, text="Delete Selected", bootstyle="danger-outline", command=self.delete_selected).pack(side=LEFT)

        table_frame = Frame(self)
        table_frame.pack(fill=BOTH, expand=YES)

        columns = ("id", "name", "date", "contact", "severity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        headings = [("id", "ID"), ("name", "Full Name"), ("date", "Diagnosis Date"),
                    ("contact", "Contact Info"), ("severity", "Case Severity")]
        for col, title in headings:
            self.tree.heading(col, text=title, command=lambda _col=col: self.sort_column(_col, False))

        for col in columns:
            self.tree.column(col, anchor=W, stretch=YES)
        self.tree.column("id", width=0, stretch=False)

        vsb = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree.bind("<Button-1>", self.clear_selection_on_blank_click)

        self.load_cases()

    def load_cases(self, records=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = records if records else fetch_all_cases()
        for case in data:
            self.tree.insert("", END, values=case)

    def apply_filters(self):
        search_text = self.search_var.get().strip().lower()
        severity = self.severity_filter.get()

        filtered = []
        for case in fetch_all_cases():
            _, name, date, contact, sev = case
            if (
                (not search_text or any(search_text in val.lower() for val in [name, date, contact, sev])) and
                (not severity or sev == severity)
            ):
                filtered.append(case)

        self.load_cases(filtered)

    def reset_filters(self):
        self.search_var.set("")
        self.severity_filter.set("")
        self.load_cases()

    def sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children()]
        data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a case to edit.")
            return

        values = self.tree.item(selected[0], "values")
        case_id, name, date, contact, severity = values

        top = Toplevel(self)
        top.title("Edit Case")
        top.geometry("400x300")
        top.grab_set()

        vars = {
            "name": StringVar(value=name),
            "date": StringVar(value=date),
            "contact": StringVar(value=contact),
            "severity": StringVar(value=severity)
        }

        Label(top, text="Full Name").pack(anchor=NW, padx=10, pady=(10, 0))
        Entry(top, textvariable=vars["name"]).pack(fill=X, padx=10)

        Label(top, text="Diagnosis Date").pack(anchor=NW, padx=10, pady=(10, 0))
        Entry(top, textvariable=vars["date"]).pack(fill=X, padx=10)

        Label(top, text="Contact Info").pack(anchor=NW, padx=10, pady=(10, 0))
        Entry(top, textvariable=vars["contact"]).pack(fill=X, padx=10)

        Label(top, text="Case Severity").pack(anchor=NW, padx=10, pady=(10, 0))
        Combobox(top, textvariable=vars["severity"], values=["Mild", "Moderate", "Severe"], state="readonly").pack(fill=X, padx=10)

        def update():
            update_case(case_id, vars["name"].get(), vars["date"].get(), vars["contact"].get(), vars["severity"].get())
            top.destroy()
            self.load_cases()

        Button(top, text="Save", bootstyle="success", command=update).pack(pady=20)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a case to delete.")
            return

        case_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this case?")
        if confirm:
            delete_case_by_id(case_id)
            self.load_cases()

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Full Name", "Diagnosis Date", "Contact Info", "Case Severity"])
            for row_id in self.tree.get_children():
                values = self.tree.item(row_id, "values")[1:]
                writer.writerow(values)

    def clear_selection_on_blank_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            self.tree.selection_remove(self.tree.selection())
