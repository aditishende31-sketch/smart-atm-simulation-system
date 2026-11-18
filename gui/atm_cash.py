
from copy import error
from dbm import error
import tkinter as tk
from tkinter import ttk, messagebox

from banking.service import admin_get_atm_cash_summary

class ATMCashWindow:

    def __init__(self, parent, session):

        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("ATM Cash Management")
        self.window.geometry("650x500")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_cash_details()

    def create_widgets(self):

        main_frame = tk.Frame(
            self.window,
            padx=30,
            pady=25
        )

        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame,
            text="🏧 ATM Cash Management",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        tk.Label(
            main_frame,
            text="Available Cash Inside ATM",
            font=("Arial", 12)
        ).pack(pady=5)

        self.total_label = tk.Label(
            main_frame,
            text="₹0",
            font=("Arial", 26, "bold"),
            fg="green"
        )

        self.total_label.pack(pady=15)

        columns = ("denomination", "quantity", "value")

        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            height=6
        )

        self.tree.heading("denomination", text="Denomination")
        self.tree.heading("quantity", text="Available Notes")
        self.tree.heading("value", text="Total Value")

        self.tree.column("denomination", anchor="center", width=170)
        self.tree.column("quantity", anchor="center", width=170)
        self.tree.column("value", anchor="center", width=170)

        self.tree.pack(fill="x", pady=15)

        tk.Button(
            main_frame,
            text="REFRESH",
            command=self.load_cash_details,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(fill="x", pady=10, ipady=6)

        tk.Button(
            main_frame,
            text="CLOSE",
            command=self.window.destroy,
            cursor="hand2"
        ).pack(fill="x", ipady=5)

    def load_cash_details(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            cash_details, total_cash = admin_get_atm_cash_summary(
                self.session
            )

            self.total_label.config(
                text=f"₹{total_cash:,.2f}"
            )

            for denomination, quantity in cash_details:

                total_value = denomination * quantity

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        f"₹{denomination}",
                        quantity,
                        f"₹{total_value:,.2f}"
                    )
            )

        except PermissionError as error:

            messagebox.showerror(
                "Access Denied",
                str(error),
                parent=self.window
            )

            self.window.destroy()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.window
            )