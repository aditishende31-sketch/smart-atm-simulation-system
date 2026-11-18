
import tkinter as tk
from tkinter import messagebox

from banking.service import transfer
from database.operations import get_account


class TransferWindow:

    def __init__(self, parent, session):

        self.parent = parent
        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Transfer Money")
        self.window.geometry("450x500")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        frame = tk.Frame(
            self.window,
            padx=40,
            pady=25
        )

        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="🔄",
            font=("Arial", 40)
        ).pack()

        tk.Label(
            frame,
            text="Transfer Money",
            font=("Arial", 20, "bold")
        ).pack(pady=8)

        tk.Label(
            frame,
            text=f"Your Account: {self.session.account_number}",
            font=("Arial", 10)
        ).pack(pady=(0, 15))

        tk.Label(
            frame,
            text="Receiver Account Number",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(5, 5))

        self.receiver_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center"
        )

        self.receiver_entry.pack(
            fill="x",
            ipady=7
        )

        tk.Label(
            frame,
            text="Transfer Amount (₹)",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.amount_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center"
        )

        self.amount_entry.pack(
            fill="x",
            ipady=7
        )

        tk.Button(
            frame,
            text="TRANSFER MONEY",
            font=("Arial", 12, "bold"),
            command=self.make_transfer,
            cursor="hand2"
        ).pack(
            fill="x",
            pady=(25, 10),
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

        self.receiver_entry.focus()

        self.window.bind(
            "<Return>",
            lambda event: self.make_transfer()
        )

    def make_transfer(self):

        receiver_number = (
            self.receiver_entry.get().strip()
        )

        amount_text = self.amount_entry.get().strip()

        if not receiver_number or not amount_text:
            messagebox.showwarning(
                "Missing Details",
                "Please enter the receiver account number "
                "and transfer amount.",
                parent=self.window
            )
            return

        if receiver_number == str(self.session.account_number):
            messagebox.showwarning(
                "Invalid Receiver",
                "You cannot transfer money to your own account.",
                parent=self.window
            )
            return

        try:
            amount = int(amount_text)
        except ValueError:
            messagebox.showwarning(
                "Invalid Amount",
                "Enter a valid whole-number amount.",
                parent=self.window
            )
            return

        if amount <= 0:
            messagebox.showwarning(
                "Invalid Amount",
                "Transfer amount must be greater than zero.",
                parent=self.window
            )
            return

        try:
            receiver = get_account(receiver_number)

            if receiver is None:
                messagebox.showerror(
                    "Receiver Not Found",
                    "No account exists with that account number.",
                    parent=self.window
                )
                return

            receiver_account_id = receiver[0]
            receiver_status = receiver[5]

            if receiver_status != "ACTIVE":
                messagebox.showerror(
                    "Account Unavailable",
                    "The receiver's account is not active.",
                    parent=self.window
                )
                return

        except Exception as error:
            messagebox.showerror(
                "Account Lookup Failed",
                str(error),
                parent=self.window
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Transfer",
            f"Transfer ₹{amount:,.2f} to account "
            f"{receiver_number}?",
            parent=self.window
        )

        if not confirmed:
            return

        try:
            sender_balance, receiver_balance = transfer(
                self.session.account_id,
                receiver_account_id,
                amount
            )

            messagebox.showinfo(
                "Transfer Successful",
                f"₹{amount:,.2f} transferred successfully.\n\n"
                f"Receiver Account: {receiver_number}\n"
                f"Your Remaining Balance: ₹{sender_balance:,.2f}",
                parent=self.window
            )

            self.window.destroy()

        except Exception as error:
            messagebox.showerror(
                "Transfer Failed",
                str(error),
                parent=self.window
            )
