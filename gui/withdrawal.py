from dbm import error
import tkinter as tk
from tkinter import messagebox

from banking.service import withdraw


class WithdrawalWindow:

    def __init__(self, parent, session):

        self.parent = parent
        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Withdraw Money")
        self.window.geometry("450x420")
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
            text="🏧",
            font=("Arial", 45)
        ).pack()

        tk.Label(
            frame,
            text="Withdraw Money",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Enter withdrawal amount",
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            pady=(20, 5)
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

        tk.Label(
            frame,
            text="Available denominations: ₹500, ₹200, ₹100",
            font=("Arial", 9)
        ).pack(pady=10)

        withdraw_button = tk.Button(
            frame,
            text="WITHDRAW",
            font=("Arial", 12, "bold"),
            command=self.make_withdrawal,
            cursor="hand2"
        )

        withdraw_button.pack(
            fill="x",
            pady=(20, 10),
            ipady=8
        )

        cancel_button = tk.Button(
            frame,
            text="CANCEL",
            command=self.window.destroy,
            cursor="hand2"
        )

        cancel_button.pack(
            fill="x",
            ipady=5
        )

        self.amount_entry.focus()

        self.window.bind(
            "<Return>",
            lambda event: self.make_withdrawal()
        )

    
    def make_withdrawal(self):

        amount_text = self.amount_entry.get().strip()

        if not amount_text:
            messagebox.showwarning(
                "Invalid Amount",
                "Please enter a withdrawal amount."
            )
            return

        try:
            amount = int(amount_text)

        except ValueError:
            messagebox.showwarning(
                "Invalid Amount",
                "Please enter a valid whole number."
            )
            return

        if amount <= 0:
            messagebox.showwarning(
                "Invalid Amount",
                "Withdrawal amount must be greater than zero."
            )
            return

        if amount % 100 != 0:
            messagebox.showwarning(
                "Invalid Amount",
                "Withdrawal amount must be in multiples of ₹100."
            )
            return

        try:
            transaction_id, new_balance = withdraw(
                self.session.account_id,
                amount
            )

            self.show_success(amount, new_balance)

            self.window.destroy()

        except Exception as error:
            messagebox.showerror(
                "Withdrawal Failed",
                str(error),
                parent=self.window
            )

    
    def show_success(self, amount, new_balance):

        messagebox.showinfo(
            "Withdrawal Successful",
            f"₹{amount:,.2f} withdrawn successfully.\n\n"
            f"Remaining Balance: ₹{new_balance:,.2f}",
            parent=self.window
        )
