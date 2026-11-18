
import tkinter as tk
from tkinter import messagebox

from database.operations import get_account


class BalanceWindow:
    def __init__(self, root, session):
        self.root = root
        self.session = session

        self.window = tk.Toplevel(root)
        self.window.title("Smart ATM - Account Balance")
        self.window.geometry("420x300")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, padx=30, pady=25)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="ACCOUNT BALANCE",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 20))

        tk.Label(
            frame,
            text=f"Account: {self.session.account_number}",
            font=("Arial", 11)
        ).pack(pady=5)

        try:
            account = get_account(self.session.account_number)

            if account is None:
                messagebox.showerror(
                    "Error",
                    "Account could not be found.",
                    parent=self.window
                )
                balance_text = "Unavailable"
            else:
                # The balance is the fifth item in the account tuple.
                balance = float(account[4])
                balance_text = f"₹ {balance:,.2f}"

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not retrieve balance:\n{error}",
                parent=self.window
            )
            balance_text = "Unavailable"

        tk.Label(
            frame,
            text=balance_text,
            font=("Arial", 25, "bold")
        ).pack(pady=20)

        tk.Button(
            frame,
            text="CLOSE",
            width=15,
            command=self.window.destroy
        ).pack(pady=10)
