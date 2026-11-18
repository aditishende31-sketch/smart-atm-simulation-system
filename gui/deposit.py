import tkinter as tk
from tkinter import messagebox

from banking.service import deposit


class DepositWindow:

    def __init__(self, parent, session):

        self.parent = parent
        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Deposit Money")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        frame = tk.Frame(
            self.window,
            padx=40,
            pady=35
        )

        frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            frame,
            text="💵",
            font=("Arial", 45)
        ).pack()

        tk.Label(
            frame,
            text="Deposit Money",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Enter Amount",
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.amount_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            justify="center"
        )

        self.amount_entry.pack(
            fill="x",
            ipady=8
        )

        tk.Button(
            frame,
            text="DEPOSIT",
            font=("Arial", 12, "bold"),
            command=self.make_deposit,
            cursor="hand2"
        ).pack(
            fill="x",
            pady=20,
            ipady=8
        )

        tk.Button(
            frame,
            text="CANCEL",
            command=self.window.destroy,
            cursor="hand2"
        ).pack(
            fill="x",
            ipady=5
        )

        self.amount_entry.focus()

    def make_deposit(self):

        amount_text = self.amount_entry.get().strip()

        if not amount_text:

            messagebox.showwarning(
                "Invalid Amount",
                "Please enter an amount."
            )
            return

        try:

            amount = float(amount_text)

        except ValueError:

            messagebox.showwarning(
                "Invalid Amount",
                "Please enter a valid number."
            )
            return

        if amount <= 0:

            messagebox.showwarning(
                "Invalid Amount",
                "Amount must be greater than zero."
            )
            return

        try:

            _, new_balance = deposit(
                self.session.account_id,
                amount
            )

            messagebox.showinfo(
                "Deposit Successful",
                f"₹ {amount:,.2f} deposited successfully.\n\n"
                f"New Balance: ₹ {new_balance:,.2f}"
            )

            self.window.destroy()

        except Exception as error:

            messagebox.showerror(
                "Deposit Failed",
                str(error)
            )