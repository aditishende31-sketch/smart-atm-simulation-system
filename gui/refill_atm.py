
import tkinter as tk
from tkinter import messagebox
import traceback

from banking.service import admin_refill_atm_cash

class RefillATMWindow:

    def __init__(self, parent, session):

        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Refill ATM Cash")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        self.entries = {}

        tk.Label(
            self.window,
            text="REFILL ATM CASH",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        for denomination in (500, 200, 100):

            tk.Label(
                self.window,
                text=f"Number of ₹{denomination} notes to add:",
                font=("Arial", 11)
            ).pack(pady=5)

            entry = tk.Entry(
                self.window,
                font=("Arial", 12),
                justify="center"
            )

            entry.pack(pady=5)

            self.entries[denomination] = entry

        tk.Button(
            self.window,
            text="REFILL CASH",
            font=("Arial", 12, "bold"),
            command=self.refill
        ).pack(pady=20)

    def refill(self):

        try:

            quantities = {}

            for denomination, entry in self.entries.items():

                value = entry.get().strip()

                quantity = int(value or "0")

                if quantity < 0:
                    raise ValueError(
                        "Number of notes cannot be negative."
                    )

                quantities[denomination] = quantity

            if not any(quantities.values()):
                raise ValueError(
                    "Enter at least one note quantity."
                )

            admin_refill_atm_cash(self.session, quantities)

            messagebox.showinfo(
                "Success",
                "ATM cash refilled successfully!",
                parent=self.window
            )

            self.window.destroy()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Input",
                str(error),
                parent=self.window
            )

        except Exception as error:
            traceback.print_exc()
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.window
            )
