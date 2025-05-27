import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ui.main_menu import MainMenu
from ui.login import LoginScreen
from database import init_db

def main():
    init_db()

    app = tb.Window(themename="flatly")
    app.title("HIV/AIDS Case Management System")
    app.geometry("1000x600")
    app.resizable(False, False)

    def launch_main_menu():
        for widget in app.winfo_children():
            widget.destroy()
        MainMenu(app).pack(fill=BOTH, expand=YES)

    LoginScreen(app, on_success=launch_main_menu)

    app.mainloop()

if __name__ == "__main__":
    main()
