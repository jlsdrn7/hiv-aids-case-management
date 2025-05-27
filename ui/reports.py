import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import *
from tkinter import filedialog
from database import fetch_all_cases
import csv
import subprocess
import sys
import tempfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Reports(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        self.start_date = StringVar()
        self.end_date = StringVar()

        Label(self, text="Reports", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 10))

        date_filter = Frame(self)
        date_filter.pack(anchor=NW, pady=(0, 15))

        Label(date_filter, text="Start Date (YYYY-MM-DD)").pack(side=LEFT, padx=(0, 5))
        start_entry = Entry(date_filter, textvariable=self.start_date, width=15)
        start_entry.pack(side=LEFT)
        start_entry.bind("<Button-1>", lambda e: self.show_calendar(self.start_date))

        Label(date_filter, text="End Date (YYYY-MM-DD)").pack(side=LEFT, padx=(20, 5))
        end_entry = Entry(date_filter, textvariable=self.end_date, width=15)
        end_entry.pack(side=LEFT)
        end_entry.bind("<Button-1>", lambda e: self.show_calendar(self.end_date))

        Button(date_filter, text="Generate", bootstyle="primary", command=self.generate_report).pack(side=LEFT, padx=(20, 5))
        Button(date_filter, text="Export CSV", bootstyle="secondary-outline", command=self.export_csv).pack(side=LEFT)

        self.summary_label = Label(self, text="", font=("Segoe UI", 12))
        self.summary_label.pack(anchor=NW, pady=(10, 20))

        self.graph_frame = Frame(self)
        self.graph_frame.pack(fill=BOTH, expand=YES)

        self.report_data = []

    def show_calendar(self, var):
        import tempfile

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        temp_path = temp_file.name
        temp_file.close()

        calendar_script = f'''
import tkinter as tk
from tkcalendar import Calendar

def select_date():
    date = cal.get_date()
    with open(r"{temp_path}", "w") as f:
        f.write(date)
    root.destroy()

root = tk.Tk()
root.title("Pick Date")
root.geometry("250x220")
cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
cal.pack(padx=10, pady=10)
tk.Button(root, text="Select", command=select_date).pack(pady=(0, 10))
root.mainloop()
'''

        subprocess.run([sys.executable, "-c", calendar_script])

        try:
            with open(temp_path, "r") as f:
                var.set(f.read().strip())
        except Exception:
            pass

    def generate_report(self):
        all_cases = fetch_all_cases()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()

        filtered = []
        for case in all_cases:
            _, name, date, contact, severity = case
            if (not start or date >= start) and (not end or date <= end):
                filtered.append(case)

        self.report_data = filtered
        total = len(filtered)
        mild = sum(1 for c in filtered if c[4].lower() == "mild")
        moderate = sum(1 for c in filtered if c[4].lower() == "moderate")
        severe = sum(1 for c in filtered if c[4].lower() == "severe")

        self.summary_label.config(text=(
            f"Total Cases: {total}\n"
            f"Mild: {mild}   Moderate: {moderate}   Severe: {severe}"
        ))

        self.show_chart(mild, moderate, severe)

    def show_chart(self, mild, moderate, severe):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        categories = ["Mild", "Moderate", "Severe"]
        values = [mild, moderate, severe]
        ax.bar(categories, values)
        ax.set_ylabel("Number of Cases")
        ax.set_title("Case Severity Breakdown")

        chart = FigureCanvasTkAgg(fig, master=self.graph_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=BOTH, expand=YES)

    def export_csv(self):
        if not self.report_data:
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Full Name", "Diagnosis Date", "Contact Info", "Case Severity"])
            for row in self.report_data:
                writer.writerow(row[1:])
