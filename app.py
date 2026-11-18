import tkinter as tk

from database.database import initialize_database
from gui.login import LoginWindow
from database.operations import initialize_atm_cash


def main():

    # Initialize database
    initialize_database()

    # Start GUI
    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":

    initialize_atm_cash()
    main()